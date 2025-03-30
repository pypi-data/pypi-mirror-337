
import traits.api as tr
from .editors import EditorFactory
import ipywidgets as ipw
import numpy as np
import time
from functools import reduce
from threading import Thread

class HistoryEditor(EditorFactory):
    """
    Progress bar running between 0 and 1 by default
    """
    label = 'history'
    var = tr.Str('t')
    min_value = tr.Float(0)
    max_value = tr.Float(1)
    step = tr.Float(0.01)
    min_var = tr.Str('')
    max_var = tr.Str('')
    step = tr.Str('')

    tooltip = tr.Property(depends_on='time_var, time_max_var')
    @tr.cached_property
    def _get_tooltip(self):
        return 'history slider 0 -> %s -> %s' % (self.var, self.max_var)

    t_min = tr.Property
    def _get_t_min(self):
        if self.min_var == '':
            t_min = self.min_value
        else:
            t_min = getattr(self.model, str(self.min_var))
        return t_min

    t_max = tr.Property
    def _get_t_max(self):
        if self.max_var == '':
            t_max = self.max_value
        else:
            t_max = getattr(self.model, str(self.max_var))
        return t_max

    step = tr.Property
    def _get_step(self):
        if self.step == '':
            step = self.step
        else:
            step = getattr(self.model, str(self.step))
        return step

    submodel = tr.Property
    def _get_submodel(self):
        submodel_path = tuple(str(self.var).split('.')[:-1])
        return reduce(lambda obj, attr: getattr(obj, attr, None), submodel_path, self.model)

    def render(self):
        history_bar_widgets = []
        var = str(self.var).split('.')[-1]
        t_span = self.t_max - self.t_min
        eta = (getattr(self.submodel, var) - self.t_min) / t_span
        t_value = eta * t_span + self.t_min
        self.history_slider = ipw.FloatSlider(
            value=eta,
            min=self.t_min,
            max=self.t_max,
            step=0.01 * t_span,
            tooltip=self.tooltip,
            continuous_update=False,
            description=self.label,
            disabled=self.disabled,
            # readout=self.readout,
            # readout_format=self.readout_format
            layout = ipw.Layout(display='flex', width="100%")
        )

        def change_time_var(event):
            eta = event['new']
            t = self.t_min + (self.t_max - self.t_min) * eta
            var = str(self.var).split('.')[-1]
            setattr(self.submodel, var, t)
            app_window = self.controller.app_window
            app_window.update_plot(self.model)

        self.history_slider.observe(change_time_var,'value')

        if self.min_var != '':
            def change_t_min(event):
                t_min = event.new
                self.history_slider.min = t_min
            self.model.observe(change_t_min, self.min_var)

        if self.max_var != '':
            def change_t_max(event):
                t_max = event.new
                self.history_slider.max = t_max
            self.model.observe(change_t_max, self.max_var)

        history_bar_widgets.append(self.history_slider)
        history_box = ipw.HBox(history_bar_widgets,
                                layout=ipw.Layout(padding='0px'))
        history_box.layout.align_items = 'center'
        return history_box

    def update_from_model(self):
        var = str(self.var).split('.')[-1]
        eta = (getattr(self.submodel, var) - self.t_min) / (self.t_max - self.t_min)
        self.history_slider.value = eta
