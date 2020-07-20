#Importing libraries
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from PIL import  Image
import pandas as pd
import seaborn as sns
import itertools
import warnings
warnings.filterwarnings("ignore")
import io
import plotly.offline as py
#py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.figure_factory as ff


class Manipulation:

    @staticmethod
    def tenure_lab(telcom) :

        if telcom["tenure"] <= 12 :
            return "Tenure_0-12"
        elif (telcom["tenure"] > 12) & (telcom["tenure"] <= 24 ):
            return "Tenure_12-24"
        elif (telcom["tenure"] > 24) & (telcom["tenure"] <= 48) :
            return "Tenure_24-48"
        elif (telcom["tenure"] > 48) & (telcom["tenure"] <= 60) :
            return "Tenure_48-60"
        elif telcom["tenure"] > 60 :
            return "Tenure_gt_60"


class Eda_Plot:

    @staticmethod
    def plot_pie(column) :

        trace1 = go.Pie(values  = churn[column].value_counts().values.tolist(),
                        labels  = churn[column].value_counts().keys().tolist(),
                        hoverinfo = "label+percent+name",
                        domain  = dict(x = [0,.48]),
                        name    = "Churn Customers",
                        marker  = dict(line = dict(width = 2,
                                                   color = "rgb(243,243,243)")
                                      ),
                        hole    = .6
                       )
        trace2 = go.Pie(values  = not_churn[column].value_counts().values.tolist(),
                        labels  = not_churn[column].value_counts().keys().tolist(),
                        hoverinfo = "label+percent+name",
                        marker  = dict(line = dict(width = 2,
                                                   color = "rgb(243,243,243)")
                                      ),
                        domain  = dict(x = [.52,1]),
                        hole    = .6,
                        name    = "Non churn customers"
                       )


        layout = go.Layout(dict(title = column + " distribution in customer attrition ",
                                plot_bgcolor  = "rgb(243,243,243)",
                                paper_bgcolor = "rgb(243,243,243)",
                                annotations = [dict(text = "churn customers",
                                                    font = dict(size = 13),
                                                    showarrow = False,
                                                    x = .15, y = .5),
                                               dict(text = "Non churn customers",
                                                    font = dict(size = 13),
                                                    showarrow = False,
                                                    x = .88,y = .5
                                                   )
                                              ]
                               )
                          )
        data = [trace1,trace2]
        fig  = go.Figure(data = data,layout = layout)
        py.iplot(fig)




    @staticmethod
    def histogram(column) :
        trace1 = go.Histogram(x  = churn[column],
                              histnorm= "percent",
                              name = "Churn Customers",
                              marker = dict(line = dict(width = .5,
                                                        color = "black"
                                                        )
                                            ),
                             opacity = .9
                             )

        trace2 = go.Histogram(x  = not_churn[column],
                              histnorm = "percent",
                              name = "Non churn customers",
                              marker = dict(line = dict(width = .5,
                                                  color = "black"
                                                 )
                                     ),
                              opacity = .9
                             )

        data = [trace1,trace2]
        layout = go.Layout(dict(title =column + " distribution in customer attrition ",
                                plot_bgcolor  = "rgb(243,243,243)",
                                paper_bgcolor = "rgb(243,243,243)",
                                xaxis = dict(gridcolor = 'rgb(255, 255, 255)',
                                                 title = column,
                                                 zerolinewidth=1,
                                                 ticklen=5,
                                                 gridwidth=2
                                                ),
                                yaxis = dict(gridcolor = 'rgb(255, 255, 255)',
                                                 title = "percent",
                                                 zerolinewidth=1,
                                                 ticklen=5,
                                                 gridwidth=2
                                                ),
                               )
                          )
        fig  = go.Figure(data=data,layout=layout)

        py.iplot(fig)


    @staticmethod
    def scatter_matrix(df)  :

        df  = df.sort_values(by = "Churn" ,ascending = True)
        classes = df["Churn"].unique().tolist()
        classes

        class_code  = {classes[k] : k for k in range(2)}
        class_code

        color_vals = [class_code[cl] for cl in df["Churn"]]
        color_vals

        pl_colorscale = "Portland"

        pl_colorscale

        text = [df.loc[k,"Churn"] for k in range(len(df))]
        text

        trace = go.Splom(dimensions = [dict(label  = "tenure",
                                           values = df["tenure"]),
                                      dict(label  = 'MonthlyCharges',
                                           values = df['MonthlyCharges']),
                                      dict(label  = 'TotalCharges',
                                           values = df['TotalCharges'])],
                         text = text,
                         marker = dict(color = color_vals,
                                       colorscale = pl_colorscale,
                                       size = 3,
                                       showscale = False,
                                       line = dict(width = .1,
                                                   color='rgb(230,230,230)'
                                                  )
                                      )
                        )
        axis = dict(showline  = True,
                    zeroline  = False,
                    gridcolor = "#fff",
                    ticklen   = 4
                   )

        layout = go.Layout(dict(title  =
                                "Scatter plot matrix for Numerical columns for customer attrition",
                                autosize = False,
                                height = 800,
                                width  = 800,
                                dragmode = "select",
                                hovermode = "closest",
                                plot_bgcolor  = 'rgba(240,240,240, 0.95)',
                                xaxis1 = dict(axis),
                                yaxis1 = dict(axis),
                                xaxis2 = dict(axis),
                                yaxis2 = dict(axis),
                                xaxis3 = dict(axis),
                                yaxis3 = dict(axis),
                               )
                          )
        data   = [trace]
        fig = go.Figure(data = data,layout = layout )
        py.iplot(fig)




    @staticmethod
    def plot_tenure_scatter(tenure_group,color) :
        tracer = go.Scatter(x = telcom[telcom["tenure_group"] == tenure_group]["MonthlyCharges"],
                            y = telcom[telcom["tenure_group"] == tenure_group]["TotalCharges"],
                            mode = "markers",marker = dict(line = dict(color = "black",
                                                                       width = .2),
                                                           size = 4 , color = color,
                                                           symbol = "diamond-dot",
                                                          ),
                            name = tenure_group,
                            opacity = .9
                           )
        return tracer


    @staticmethod
    def plot_churncharges_scatter(churn,color) :
        tracer = go.Scatter(x = telcom[telcom["Churn"] == churn]["MonthlyCharges"],
                            y = telcom[telcom["Churn"] == churn]["TotalCharges"],
                            mode = "markers",marker = dict(line = dict(color = "black",
                                                                       width = .2),
                                                           size = 4 , color = color,
                                                           symbol = "diamond-dot",
                                                          ),
                            name = "Churn - " + churn,
                            opacity = .9
                           )
        return tracer


    @staticmethod
    def layout_title(title) :
        layout = go.Layout(dict(title = title,
                                plot_bgcolor  = "rgb(243,243,243)",
                                paper_bgcolor = "rgb(243,243,243)",
                                xaxis = dict(gridcolor = 'rgb(255, 255, 255)',
                                             title = "Monthly charges",
                                             zerolinewidth=1,ticklen=5,gridwidth=2),
                                yaxis = dict(gridcolor = 'rgb(255, 255, 255)',
                                             title = "Total Charges",
                                             zerolinewidth=1,ticklen=5,gridwidth=2),
                                height = 600
                               )
                          )
        return layout


    @staticmethod
    def mean_charges(column,aggregate) :
        tracer = go.Bar(x = avg_tgc[avg_tgc["Churn"] == aggregate]["tenure_group"],
                        y = avg_tgc[avg_tgc["Churn"] == aggregate][column],
                        name = aggregate,marker = dict(line = dict(width = 1)),
                        text = "Churn"
                       )
        return tracer


    @staticmethod
    def layout_plot(title,xaxis_lab,yaxis_lab) :
        layout = go.Layout(dict(title = title,
                                plot_bgcolor  = "rgb(243,243,243)",
                                paper_bgcolor = "rgb(243,243,243)",
                                xaxis = dict(gridcolor = 'rgb(255, 255, 255)',title = xaxis_lab,
                                             zerolinewidth=1,ticklen=5,gridwidth=2),
                                yaxis = dict(gridcolor = 'rgb(255, 255, 255)',title = yaxis_lab,
                                             zerolinewidth=1,ticklen=5,gridwidth=2),
                               )
                          )
        return layout
