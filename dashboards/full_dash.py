from collections import OrderedDict 
from inspect import signature

from dash.dependencies import Input, Output,State
from dash.exceptions import PreventUpdate
from dash import callback_context

from visual.abstract_visual import AbstractVisualiser
from dashboards.abstract_dash import AbstractDash

id_prefix = "cyto"
graph_id = "full_graph"
default_options = []
preset_inputs = OrderedDict()
preset_outputs = OrderedDict()
update_inputs = OrderedDict()


docs_modal_inputs = {"open_doc" : Input("open_doc", "n_clicks"), 
                    "close_doc" : Input("close_doc", "n_clicks")}

export_inputs              = [Input("png","n_clicks"),
                              Input("jpg","n_clicks"),
                              Input("svg","n_clicks")]

not_modifier_identifiers = {"sidebar_id" : "sidebar-left",
                            "utility_id" : "utility"}

update_outputs =           {"graph_id"   : Output("content","children"),
                            "legend_id"  : Output("sidebar-right","children")}

graph_type_outputs =       {"options_id" : Output("options","style"),
                            "div"        : Output("div","children")}

docs_modal_outputs =       {"doc_modal_id" : Output("doc_modal", "is_open")}
doc_modal_states =         State("doc_modal", "is_open")

export_outputs =           Output(graph_id, "generateImage")

assets_ignore='.*bootstrap.*'
class FullDash(AbstractDash):
    def __init__(self,graph_visualiser,name,server,pathname):
        super().__init__(graph_visualiser,name,server,pathname,assets_ignore=assets_ignore)
        self._build_app()

    def _load_graph(self):
        figure_layout_elements = {"autosize": True}
        figure,legend = self.visualiser.build(layout_elements=figure_layout_elements,graph_id=graph_id,legend=True)
        graph_div = self.create_div(update_outputs["graph_id"].component_id,[figure],className="col-10")
        legend = self.create_div(update_outputs["legend_id"].component_id,self.create_legend(legend),className="col sidebar")
        self.replace(graph_div[0])
        self.replace(legend[0])
        container = self.create_div("row-main",self.children,className="row")
        self.app.layout = self.create_div("main",container,className="container-fluid")[0]

    def _build_app(self):
        # Add Options
        visual_class = self.visualiser.__class__
        form_elements,identifiers,maps = self._create_form_elements(visual_class,default_vals=default_options,
                                                                    id_prefix=id_prefix)

        del maps["cyto_preset"]
        preset_identifiers,identifiers,preset_output,preset_state = self._generate_inputs_outputs(identifiers)
        
        update_inputs.update(identifiers)
        preset_inputs.update(preset_identifiers)
        preset_outputs.update(preset_output)
        
        # Add Graph @@'''@@@'' Graph_TYPE_OUTPUTS can be removed i think
        form_div = self.create_div(graph_type_outputs["options_id"].component_id,form_elements)
        self.create_sidebar(not_modifier_identifiers["sidebar_id"],"Options",form_div,add=True,className="col sidebar")
        self.app.layout = self.create_div("main",self.children,className="content")[0]


        # Bind the callbacks
        def update_preset_inner(preset_name,*states):
            return self.update_preset(preset_name,maps,states)
        def update_graph_inner(*args):
            return self.update_graph(args)
        def docs_modal_inner(*args):
            return self.docs_modal(*args)
        def export_graph_inner(*args):
            return self.export_graph(*args)

        self.add_callback(update_preset_inner,list(preset_inputs.values()),list(preset_outputs.values()),list(preset_state.values()))
        self.add_callback(update_graph_inner,list(update_inputs.values()),list(update_outputs.values()))
        self.add_callback(docs_modal_inner,list(docs_modal_inputs.values()),list(docs_modal_outputs.values()),doc_modal_states)
        self.add_callback(export_graph_inner,export_inputs,export_outputs)
        self.build()

    def update_preset(self,preset_name,mappings,*states):
        if preset_name is None:
            raise PreventUpdate()
        try:
            setter = getattr(self.visualiser,preset_name,None)
        except TypeError:
            raise PreventUpdate()
        states = states[0]
        modified_vals = setter()
        modified_vals = [m.__name__ for m in modified_vals]
        final_outputs = []
        for index,state in enumerate(states):
            is_modified = False
            states_possible_vals = list(mappings.items())[index][1]
            for mod in modified_vals:
                if mod in states_possible_vals:
                    final_outputs.append(mod)
                    is_modified = True
                    break 
            if not is_modified:
                final_outputs.append(state)
        return final_outputs

    def update_graph(self,*args):
        if not isinstance(self.visualiser,AbstractVisualiser):
            raise PreventUpdate()
        args = args[0]
        old_settings = self.visualiser.copy_settings()
        for index,setter_str in enumerate(args):
            if setter_str is not None:
                try:
                    setter = getattr(self.visualiser,setter_str,None)
                    parameter = None
                except TypeError:
                    # Must be a input element rather than a checkbox.
                    # With annonymous implementation this is tough.
                    to_call = list(update_inputs.keys())[index]
                    parameter = setter_str
                    setter = getattr(self.visualiser,to_call,None)                    
                if setter is not None:
                    try:
                        if parameter is not None:
                            setter(parameter)
                        else:
                            setter()
                    except Exception as ex:
                        print(ex)
                        return self.reverse_graph(old_settings,ex)
        try:
            figure,legend = self.visualiser.build(graph_id=graph_id,legend=True)
            legend = self.create_legend(legend)
            return [figure],legend
        except Exception as ex:
            print(ex)
            return self.reverse_graph(old_settings,ex)

    def export_graph(self,get_jpg_clicks, get_png_clicks, get_svg_clicks):
        action = 'store'
        input_id = None
        ctx = callback_context
        if ctx.triggered:
            input_id = ctx.triggered[0]["prop_id"].split(".")[0]
            if input_id != "tabs":
                action = "download"
        return {'type': input_id,'action': action}

    def reverse_graph(self,old_settings,error_str = ""):
        for setting in old_settings:
            if setting is not None:
                setting()
        figure,legend = self.visualiser.build(graph_id=graph_id,legend=True)
        legend = self.create_legend(legend)
        return [figure],legend

    def docs_modal(self,n1, n2, is_open):
        if n1 or n2:
            return [not is_open]
        return [is_open]

    def _create_form_elements(self,visualiser,default_vals = [],style = {},id_prefix = ""):
        default_options = [visualiser.set_network_mode,
                        visualiser.set_full_graph_view,
                        visualiser.set_spring_layout,
                        visualiser.add_node_no_labels,
                        visualiser.add_edge_no_labels,
                        visualiser.add_standard_node_color,
                        visualiser.add_standard_edge_color]
        options = self._generate_options(visualiser)
        removal_words = ["Add","Set"]
        elements = []
        identifiers = {}
        docstring = []
        variable_input_list_map = OrderedDict()
        for k,v in options.items():
            display_name = self._beautify_name(k)
            identifier = id_prefix + "_" + k
            element = []

            if isinstance(v,(int,float)):
                min_v = v/4
                max_v = v*4
                default_val = (min_v + max_v) / 2
                step = 1
                element = self.create_slider(identifier ,display_name,min_v,max_v,default_val=default_val,step=step)
                identifiers[k] =  Input(identifier,"value")
                variable_input_list_map[identifier] = [min_v,max_v]

            elif isinstance(v,dict):
                removal_words = removal_words + [word for word in display_name.split(" ")]
                inputs = []
                default_button = None
                for k1,v1 in v.items():
                    label = self._beautify_name(k1)
                    label = "".join("" if i in removal_words else i + " " for i in label.split())
                    inputs.append({"label" : label, "value" : k1})
                    if v1 in default_options:
                        default_button = k1

                variable_input_list_map[identifier] = [l["value"] for l in inputs]
                element = (self.create_heading_6(k,display_name) + 
                           self.create_radio_item(identifier,inputs,value=default_button))
                identifiers[k] = Input(identifier,"value")
                docstring += self._build_docstring(display_name,v)

            breaker = self.create_horizontal_row(False)
            elements = elements + self.create_div(identifier + "_container",element,style=style) 
            elements = elements + breaker     
        
        docstrings =  self.create_div(docs_modal_inputs["open_doc"].component_id,[],className="help-tip")
        docstrings += self.create_modal(docs_modal_outputs["doc_modal_id"].component_id,
                                       docs_modal_inputs["close_doc"].component_id,
                                       "Options Documentation", docstring)

        exports = self.create_heading_4("export_heading","Export Options")
        for e_input in export_inputs:
            exports += self.create_button(e_input.component_id,className="export_button")
            exports += self.create_line_break()
        export_div = self.create_div("export_container",exports,style=style)

        return elements + export_div + docstrings, identifiers, variable_input_list_map

    def _beautify_name(self,name):
        name_parts = name.split("_")
        name = "".join([p.capitalize() + " " for p in name_parts])
        return name

    def _generate_options(self,visualiser):
        visualiser = visualiser()
        blacklist_functions = ["build",
                            "mode",
                            "edge_pos",
                            "node_text_preset",
                            "edge_text_preset",
                            "node_color_preset",
                            "edge_color_preset",
                            "node_size_preset",
                            "layout",
                            "copy_settings"]

        options = {"preset" : {},
                "mode" : {},
                "view" : {},
                "layout" : {}}

        for func_str in dir(visualiser):
            if func_str[0] == "_":
                continue
            func = getattr(visualiser,func_str,None)

            if func is None or func_str in blacklist_functions or not callable(func):
                continue
            
            if len(signature(func).parameters) > 0:
                # When there is parameters a slider will be used.
                # Some Paramterised setters will return there default val if one isnt provided.
                default_val = func()
                if default_val is None:
                    default_val = 1
                options[func_str] = default_val
            else:
                # When no params radiobox.
                if func_str.split("_")[-1] == "preset":
                    option_name = "preset"

                elif func_str.split("_")[-1] == "view":
                    option_name = "view"

                elif func_str.split("_")[-1] == "mode":
                    option_name = "mode"

                elif func_str.split("_")[-1] == "layout":
                    option_name = "layout"

                elif "node" in func_str:
                    option_name = "node" + "_" + func_str.split("_")[-1]
                    
                elif "edge" in func_str:
                    option_name = "edge" + "_" + func_str.split("_")[-1]
                else:
                    option_name = "misc"
                
                if option_name not in options.keys():
                    options[option_name] = {func_str : func}
                else:
                    options[option_name][func_str] = func
        return options

    def _generate_inputs_outputs(self,identifiers):
        preset_identifiers = {"preset" : identifiers["preset"]}
        del identifiers["preset"]
        outputs = {k:Output(v.component_id,v.component_property) for k,v in identifiers.items()}
        states = {k:State(v.component_id,v.component_property) for k,v in identifiers.items()}
        return preset_identifiers,identifiers,outputs,states


    def _build_docstring(self,doc_name,functions):
        doc_body = self.create_heading_4(doc_name,doc_name)
        for name,function in functions.items():
            func_data = self.create_heading_5(name + "_doc_heading",self._beautify_name(name))
            func_doc = function.__doc__
            if func_doc is None:
                func_doc = "No Information."
            func_doc = func_doc.lstrip().rstrip().replace("    ","")
            func_data += self.create_paragraph(func_doc)
            doc_body += self.create_div(name + "_doc",func_data) + self.create_line_break()

        doc_body += self.create_horizontal_row(False)
        return self.create_div(doc_name + "_container",doc_body)