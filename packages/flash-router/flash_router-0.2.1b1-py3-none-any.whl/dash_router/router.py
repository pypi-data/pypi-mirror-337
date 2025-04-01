from functools import partial
import importlib
import json
import os
import traceback
from typing import Any, Awaitable, Callable, Dict, List, Literal, Tuple, Union
from uuid import UUID, uuid4

from dash import html
from dash._get_paths import app_strip_relative_path
from dash._grouping import map_grouping, update_args_group
from dash._utils import inputs_to_vals, convert_to_AttributeDict
from dash._validate import validate_and_group_input_args
from dash.development.base_component import Component
from flash import Flash, Input, Output, State, set_props
from flash._pages import _parse_path_variables, _parse_query_string
from quart import request
import asyncio

from ._utils import (
    create_pathtemplate_key,
    format_segment,
    path_to_module,
    recursive_to_plotly_json,
)
from .components import ChildContainer, LacyContainer, RootContainer, SlotContainer
from .models import ExecNode, PageNode, RootNode, RouteConfig, RouterResponse


class Router:
    def __init__(
        self,
        app: Flash,
        pages_folder: str = "pages",
        requests_pathname_prefix: str | None = None,
        ignore_empty_folders: bool = False,
    ) -> None:
        self.app = app
        self.static_routes = RootNode()
        self.dynamic_routes = RootNode()
        self.route_table = {}
        self.requests_pathname_prefix = requests_pathname_prefix
        self.ignore_empty_folders = ignore_empty_folders
        self.pages_folder = app.pages_folder if app.pages_folder else pages_folder

        if not isinstance(self.app, Flash):
            raise TypeError(f"App needs to be of Flash not: {type(self.app)}")

        self.setup_route_tree()
        self.setup_router()
        # self.setup_lacy_callback()

    def setup_route_tree(self) -> None:
        """Sets up the route tree by traversing the pages folder."""
        root_dir = ".".join(self.app.server.name.split(os.sep)[:-1])
        self._traverse_directory(root_dir, self.pages_folder, None)

    def _validate_node(self, node: PageNode):
        # Validate Slots

        # Validate children
        if node.default_child:
            pass

    def _validate_tree(self):
        for root_node in self.dynamic_routes.routes.items():
            self._validate_node(root_node)

    def _traverse_directory(
        self,
        parent_dir: str,
        segment: str,
        current_node: Union[RootNode, PageNode] | None,
    ) -> None:
        """Recursively traverses the directory structure and registers routes."""
        current_dir = os.path.join(parent_dir, segment)
        if not os.path.exists(current_dir):
            return

        entries = os.listdir(current_dir)
        dir_has_page = "page.py" in entries

        if dir_has_page:
            new_node = self.load_route_module(current_dir, segment, current_node)
            if new_node is not None:
                self._process_directory_with_page(current_dir, new_node, current_node)
                next_node = new_node
            else:
                next_node = current_node
        else:
            next_node = current_node

        for entry in sorted(entries):
            if entry.startswith((".", "_")) or entry == "page.py":
                continue

            full_path = os.path.join(current_dir, entry)
            if os.path.isdir(full_path):
                self._traverse_directory(current_dir, entry, next_node)

    def _process_directory_with_page(
        self,
        current_dir: str,
        new_node: PageNode,
        parent_node: Union[RootNode, PageNode] | None,
    ) -> None:
        """
        Registers a node from a directory containing a page.py.
        Registration is based on whether the node is a root, static, slot, or dynamic route.
        """
        if current_dir == self.pages_folder:
            new_node.path = "/"
            new_node.segment = "/"
            new_node.parent_segment = None
            self.static_routes.register_root_route(new_node)
        else:
            relative_path = os.path.relpath(current_dir, self.pages_folder)
            if new_node.path_template:
                relative_path = f"{relative_path}/{new_node.path_template}"
            relative_path = format_segment(relative_path)
            new_node.path = relative_path

            if new_node.is_static:
                self.static_routes.register_root_route(new_node)

            elif new_node.is_root:
                self.dynamic_routes.register_root_route(new_node)

            elif new_node.is_slot:
                parent_node.register_slot(new_node)

            else:
                parent_node.register_route(new_node)

    def load_route_module(
        self, current_dir: str, segment: str, parent_node: PageNode
    ) -> PageNode | None:
        is_root = parent_node is None or parent_node.segment == "/"
        segment = "/" if not parent_node else segment
        parent_segment = parent_node.segment if parent_node else "/"
        page_module_name = path_to_module(current_dir, "page.py")

        page_layout = self.import_route_component(current_dir, "page.py")
        loading_layout = self.import_route_component(current_dir, "loading.py")
        endpoint = self.import_route_component(current_dir, "api.py", "endpoint")
        error_layout = (
            self.import_route_component(current_dir, "error.py") or self.app._on_error
        )
        route_config = (
            self.import_route_component(current_dir, "page.py", "config")
            or RouteConfig()
        )

        is_slot = segment.startswith("(") and segment.endswith(")")
        formatted_segment = format_segment(segment, is_slot)
        node_id = uuid4()
        new_node = PageNode(
            node_id=node_id,
            layout=page_layout,
            segment=formatted_segment,
            parent_segment=parent_segment,
            module=page_module_name,
            is_slot=is_slot,
            is_static=route_config.is_static,
            is_root=is_root,
            error=error_layout,
            loading=loading_layout,
            endpoint=endpoint
        )   

        self.route_table[node_id] = new_node

        new_node.load_config(route_config)
        return new_node

    def strip_relative_path(self, path: str) -> str:
        return app_strip_relative_path(self.app.config.requests_pathname_prefix, path)

    def import_route_component(
        self,
        current_dir: str,
        file_name: Literal["page.py", "error.py", "loading.py", "api.py"],
        component_name: Literal["layout", "config", 'endpoint'] = "layout",
    ) -> Callable[..., Component] | Component | None:
        page_module_name = path_to_module(current_dir, file_name)
        try:
            page_module = importlib.import_module(page_module_name)
            layout = getattr(page_module, component_name, None)
            if file_name == "page.py" and not layout:
                raise ImportError(
                    f"Module {page_module_name} needs a layout function or component"
                )
            return layout

        except ImportError as e:
            if file_name == "layout.py":
                print(f"Error processing {page_module_name}: {e}")
                print(f"Traceback: {traceback.format_exc()}")
                raise ImportError(
                    f"Module {page_module_name} needs a layout function or component"
                )
        except Exception as e:
            print(f"Error processing {page_module_name}: {e}")
            print(f"Traceback: {traceback.format_exc()}")

        return None

    def get_static_route(self, path: str) -> Tuple[PageNode | None, Any]:
        path_variables: Any = None
        for root_page in self.static_routes.routes.values():
            if root_page.path_template:
                path_variables = _parse_path_variables(path, root_page.path)
                if path_variables:
                    return root_page, path_variables
            if path == root_page.path:
                return root_page, path_variables
        return None, path_variables

    def _get_root_node(
        self, segments: List[str], loading_state: Dict[str, bool]
    ) -> Tuple[PageNode | None, List[str], Dict[str, bool], Dict[str, str]]:
        """
        Iterates through URL segments to find the matching root node.
        Returns:
          - The active PageNode (or None if not found),
          - The remaining segments,
          - An updated loading state mapping, and
          - Any extracted path variables.
        """
        remaining_segments = segments.copy()
        updated_segments: Dict[str, bool] = {}
        variables: Dict[str, str] = {}
        active_node: PageNode | None = None

        def compute_key(node: PageNode, segment: str) -> str:
            if node.path_template:
                return create_pathtemplate_key(
                    node.segment,
                    node.path_template,
                    segment,
                    node.path_template.strip("<>"),
                )
            return segment

        while remaining_segments:
            segment = remaining_segments[0]
            print('Processing Segment', segment, sep=':', flush=True)
            if active_node is None:
                active_node = self.dynamic_routes.get_route(segment)
                if not active_node:
                    return None, [], {}, {}
                key = compute_key(active_node, segment)
                segment_loading_state = loading_state.get(key, False)
                remaining_segments.pop(0)
                if not segment_loading_state:  # or segment_loading_state == "lacy"
                    return active_node, remaining_segments, updated_segments, variables
                updated_segments[key] = True
                continue

            child_node = active_node.get_child_node(segment, self.route_table)
            if not child_node:
                if not self.ignore_empty_folders and len(remaining_segments) > 1:
                    first = remaining_segments.pop(0)
                    second = remaining_segments.pop(0)
                    combined = f"{first}/{second}"
                    remaining_segments.insert(0, combined)
                    continue
                remaining_segments.pop(0)
                continue

            key = compute_key(child_node, segment)
            segment_loading_state = loading_state.get(key, False)
            active_node = child_node

            if not segment_loading_state:
                if child_node.segment == key:
                    remaining_segments.pop(0)
                return active_node, remaining_segments, updated_segments, variables

            if child_node.path_template and remaining_segments:
                if len(remaining_segments) == 1:
                    return active_node, remaining_segments, updated_segments, variables
                if child_node.path_template == "<...rest>":
                    variables["rest"] = remaining_segments
                    return active_node, [], updated_segments, variables

                variables[child_node.path_template.strip("<>")] = segment

            updated_segments[key] = True
            remaining_segments.pop(0)

        return active_node, remaining_segments, updated_segments, variables

    def build_execution_tree(
        self,
        current_node: PageNode,
        segments: List[str],
        parent_variables: Dict[str, str],
        query_params: Dict[str, Any],
        loading_state: Dict[str, bool],
        request_pathname: str,
        endpoints: Dict[UUID, Callable[..., Awaitable[any]]],
        is_init: bool
    ) -> Tuple[ExecNode, Dict[UUID, Callable[..., Awaitable[any]]]]:
        """
        Recursively builds the execution tree for the matched route.
        It extracts any path variables, processes child nodes, and handles slot nodes.
        """
        current_variables = {**parent_variables, **query_params}
        if segments and current_node.path_template:
            next_segment = segments[0]
            varname = current_node.path_template.strip("<>")
            segments = segments[1:]
            if current_node.path_template == "<...rest>":
                varname = "rest"
                next_segment = (
                    [next_segment] + segments
                    if next_segment != current_node.segment
                    else segments
                )
                segments = []

            current_variables[varname] = next_segment

        exec_node = ExecNode(
            node_id=current_node.node_id,
            layout=current_node.layout,
            segment=current_node.segment,
            parent_segment=current_node.parent_segment,
            variables=current_variables,
            loading_state=loading_state,
            path_template=current_node.path_template,
            loading=current_node.loading,
            error=current_node.error,
            path=request_pathname,
        )

        if current_node.endpoint and not is_init and current_node.loading:
            partial_endpoint = partial(current_node.endpoint, **current_variables)
            endpoints[current_node.node_id] = partial_endpoint
        
        if current_node.endpoint and not current_node.loading:
            partial_endpoint = partial(current_node.endpoint, **current_variables)
            endpoints[current_node.node_id] = partial_endpoint

        if current_node.child_nodes:
            child_exec = self._process_child_node(
                current_node=current_node,
                segments=segments.copy(),
                current_variables=current_variables,
                query_params=query_params,
                loading_state=loading_state,
                requests_pathname=request_pathname,
                endpoints=endpoints,
                is_init=is_init,
            )
            exec_node.child_node["children"] = child_exec

        if current_node.slots:
            exec_node.slots = self._process_slot_nodes(
                current_node=current_node,
                segments=segments.copy(),
                current_variables=current_variables,
                query_params=query_params,
                loading_state=loading_state,
                requests_pathname=request_pathname,
                endpoints=endpoints,
                is_init=is_init,            
            )
            if not segments:
                return exec_node, endpoints

        return exec_node, endpoints

    def _process_child_node(
        self,
        current_node: PageNode,
        segments: List[str],
        current_variables: Dict[str, str],
        query_params: Dict[str, Any],
        loading_state: Dict[str, bool],
        requests_pathname: str,
        endpoints: Dict[UUID, Callable[..., Awaitable[any]]],
        is_init: bool = True
    ) -> ExecNode | None:
        """Handles processing of a child view node."""
        next_segment = segments[0] if segments else None
        child_node_id = current_node.child_nodes.get(next_segment)

        if not child_node_id:
            default_segment = current_node.default_child
            child_node_id = current_node.child_nodes.get(default_segment, None)

        if child_node_id:
            if segments:
                segments = segments[1:]
            
            child_node = self.route_table.get(child_node_id)
            exec_node, _ = self.build_execution_tree(
                current_node=child_node,
                segments=segments.copy(),
                parent_variables=current_variables,
                query_params=query_params,
                loading_state=loading_state,
                request_pathname=requests_pathname,
                endpoints=endpoints,
                is_init=is_init
            )
            return exec_node
        
        return None

    def _process_slot_nodes(
        self,
        current_node: PageNode,
        segments: List[str],
        current_variables: Dict[str, str],
        query_params: Dict[str, Any],
        loading_state: Dict[str, bool],
        requests_pathname: str,
        endpoints: Dict[UUID, Callable[..., Awaitable[any]]],
        is_init: bool = True
    ) -> Dict[str, ExecNode]:
        """Processes all slot nodes defined on the current node."""
        slot_exec_nodes: Dict[str, ExecNode] = {}
        for slot_name, slot_id in current_node.slots.items():
            slot_node: PageNode = self.route_table.get(slot_id)

            if slot_node.is_slot and slot_node.path_template and not segments:
                path_key = slot_node.path_template.strip("<>")
                path_variable = current_variables.get(path_key) 
                path_variable = path_variable or 'test'
                segment_key = create_pathtemplate_key(
                    slot_node.segment, slot_node.path_template, path_variable, path_key
                )
                loading_state[segment_key] = True

            slot_exec_node, _ = self.build_execution_tree(
                current_node=slot_node,
                segments=segments.copy(),
                parent_variables=current_variables,
                query_params=query_params,
                loading_state=loading_state,
                request_pathname=requests_pathname,
                endpoints=endpoints,
                is_init=is_init
            )
            
            slot_exec_nodes[slot_name] = slot_exec_node
            
        return slot_exec_nodes

    # ─── RESPONSE BUILDER ─────────────────────────────────────
    async def dispatch(
        self,
        pathname: str,
        query_parameters: Dict[str, any],
        loading_state: Dict[str, any],
        is_init: bool = True,
    ) -> RouterResponse:
        if pathname == "/" or not pathname:
            node = self.static_routes.get_route("/")
            layout = await node.layout(**query_parameters)
            return self._build_response(
                RootContainer.ids.container, layout, {}, is_init
            )

        path = self.strip_relative_path(pathname)
        static_route, path_variables = self.get_static_route(path)
        if static_route:
            layout = await static_route.layout(
                **query_parameters, **(path_variables or {})
            )
            return self._build_response(
                RootContainer.ids.container, layout, {}, is_init
            )

        init_segments = [seg for seg in pathname.strip("/").split("/") if seg]
        active_node, remaining_segments, updated_segments, path_vars = (
            self._get_root_node(init_segments, loading_state)
        )

        if not active_node:
            return self._build_response(
                RootContainer.ids.container,
                html.H1("404 - Page not found"),
                {},
                is_init,
            )
    
        exec_tree, endpoints = self.build_execution_tree(
            current_node=active_node,
            segments=remaining_segments,
            parent_variables=path_vars,
            query_params=query_parameters,
            loading_state=updated_segments,
            request_pathname=path,
            is_init=is_init,
            endpoints={},
        )
        
        if not exec_tree:
            return self._build_response(
                RootContainer.ids.container,
                html.H1("404 - Page not found"),
                {},
                is_init,
            )

        result_data = await self.gather_endpoints(endpoints)
        final_layout = await exec_tree.execute(result_data, is_init)

        new_loading_state = {**updated_segments, **exec_tree.loading_state}
        
        container_id = RootContainer.ids.container
        if active_node.parent_segment != "/":
            if active_node.is_slot:
                container_id = json.dumps(
                    SlotContainer.ids.container(
                        active_node.parent_segment, active_node.segment
                    )
                )
            else:
                container_id = json.dumps(
                    ChildContainer.ids.container(active_node.parent_segment)
                )

        return self._build_response(
            container_id, final_layout, new_loading_state, is_init
        )
    
    @staticmethod
    async def gather_endpoints(endpoints: Dict[UUID, Callable[..., Awaitable[any]]]):
        if not endpoints:
            return {}
            
        keys = list(endpoints.keys())
        funcs = list(endpoints.values())
        results = await asyncio.gather(*[func() for func in funcs], return_exceptions=True)
        return dict(zip(keys, results))

    def _build_response(
        self,
        container_id: str,
        layout: Any,
        loading_state: Dict[str, Any] | None = None,
        is_init: bool = True,
    ) -> RouterResponse:
        """
        Wraps a rendered layout and optional state into a RouterResponse model.
        """
        if not is_init:
            set_props(RootContainer.ids.state_store, {"data": loading_state or {}})
            return layout
        rendered_layout = recursive_to_plotly_json(layout)
        response = {container_id: {"children": rendered_layout}}
        if loading_state is not None:
            response[RootContainer.ids.state_store] = {"data": loading_state}
        return RouterResponse(multi=True, response=response).model_dump()

    # ─── ASYNC & SYNC ROUTER SETUP ───────────────────────────────────────────────────
    def setup_router(self) -> None:
        @self.app.server.before_request
        async def router():
            request_data = await request.get_data()
            if not request_data:
                return

            body = json.loads(request_data)
            changed_prop = changed_prop = body.get("changedPropIds")
            changed_prop_id = changed_prop[0].split(".")[0] if changed_prop else None

            if changed_prop_id != RootContainer.ids.location:
                return

            output = body["output"]
            inputs = body.get("inputs", [])
            state = body.get("state", [])
            cb_data = self.app.callback_map[output]
            inputs_state_indices = cb_data["inputs_state_indices"]

            args = inputs_to_vals(inputs + state)
            pathname_, search_, loading_state_, states_ = args
            query_parameters = _parse_query_string(search_)
            pathname_, search_, loading_state_, states_ = args
            query_parameters = _parse_query_string(search_)
 
            _, func_kwargs = validate_and_group_input_args(
                args, inputs_state_indices
            )
            # Skip the arguments required for routing
            func_kwargs = dict(list(func_kwargs.items())[3:])
            varibales = {**query_parameters, **func_kwargs}

            try:
                return await self.dispatch(pathname_, varibales, loading_state_)
            except Exception:
                print(f"Traceback: {traceback.format_exc()}")
                raise Exception("Failed to resolve the URL")

        @self.app.server.before_serving
        async def trigger_router():
            inputs = {
                "pathname_": Input(RootContainer.ids.location, "pathname"),
                "search_": Input(RootContainer.ids.location, "search"),
                "loading_state_": State(RootContainer.ids.state_store, "data"),
            }
            inputs.update(self.app.routing_callback_inputs)

            @self.app.callback(
                Output(RootContainer.ids.dummy, "children"), inputs=inputs
            )
            async def update(
                pathname_: str, search_: str, loading_state_: str, **states
            ):
                pass

    def setup_lacy_callback(self):
        @self.app.server.before_request
        async def load_lacy():
            request_data = await request.get_data()
            if not request_data:
                return

            body = json.loads(request_data)
            component_id = body.get("outputs").get("id")
            if not isinstance(component_id, dict):
                return
            component_type = component_id.get("type")

            if not component_type == LacyContainer.ids.container("none").get("type"):
                return

            node_id = UUID(component_id.get("index"))
            inputs = body.get("inputs", [])
            state = body.get("state", [])
            args = inputs_to_vals(inputs + state)
            _, children, variables, pathname_, search_, loading_state_ = args
            query_parameters = _parse_query_string(search_)
            node_variables = json.loads(variables)

            path = self.strip_relative_path(pathname_)

            lacy_node = self.route_table.get(node_id)
            exec_tree, endpoints = self.build_execution_tree(
                current_node=lacy_node,
                segments=[],
                parent_variables=node_variables,
                query_params=query_parameters,
                loading_state=loading_state_,
                request_pathname=path,
                is_init=False,
                endpoints={}
            )

            endpoint_results = await self.gather_endpoints(endpoints)
            layout = await exec_tree.execute(is_init=False, endpoints=endpoint_results)

            container_id = RootContainer.ids.container
            if lacy_node.parent_segment != "/":
                if lacy_node.is_slot:
                    container_id = json.dumps(
                        SlotContainer.ids.container(
                            lacy_node.parent_segment, lacy_node.segment
                        )
                    )
                else:
                    container_id = json.dumps(
                        ChildContainer.ids.container(lacy_node.parent_segment)
                    )

            return self._build_response(
                container_id, layout, exec_tree.loading_state, True
            )

        # @self.app.server.before_serving
        # async def trigger_lacy():
        #     @self.app.callback(
        #         Output(LacyContainer.ids.container(MATCH), "children"),
        #         Input(LacyContainer.ids.container(MATCH), "children"),
        #         Input(LacyContainer.ids.container(MATCH), "id"),
        #         Input(LacyContainer.ids.container(MATCH), "data-path"),
        #         State(RootContainer.ids.location, "pathname"),
        #         State(RootContainer.ids.location, "search"),
        #         State(RootContainer.ids.state_store, "data"),
        #     )
        #     async def load_lacy_component(
        #         children, lacy_segment_id, variables, pathname, search, loading_state
        #     ):
        #         pass
