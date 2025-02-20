import base64

import plotly.express as px
import plotly.io as pio
from django.db.models import Sum

from code.helpers.django import generate_assessment_stars
from webapp.models import Dataset, EHDSCategory, DQDimension, DQMetric, DQMetricValue, DQCategoricalMetricCategory


def plot_label(dataset: Dataset):
    elements = []
    parents = []
    values = []

    scores, total_score = compute_scores(dataset=dataset)

    stars = generate_assessment_stars(
        total_score,
        empty_star='\u2606',
        filled_star='\u2605'
    )

    total_score = '{:.2f}'.format(total_score)

    elements.append('QUANTUM')
    parents.append('')
    values.append(100)

    for category in EHDSCategory.objects.all():
        dimensions = DQDimension.objects.filter(ehds_category=category)

        elements.append(category.name)
        parents.append('QUANTUM')
        values.append(scores[category.name]['relevance'])

        for dimension in dimensions:
            elements.append(dimension.name)
            parents.append(category.name)

            if scores[category.name]['dimensions'][dimension.name]['score'] > 0:
                score = scores[category.name]['dimensions'][dimension.name]['score']
            else:
                score = 0
            values.append(score)

    data = dict(
        elements=elements,
        parents=parents,
        values=values
    )

    # Create the sunburst plot
    figure = px.sunburst(
        data,
        names='elements',
        parents='parents',
        values='values',
        title='',
        branchvalues='total',
        # color='Score',  # Set the color to be based on the 'values'
        # color_continuous_scale=['#FFFFFF', '#123262']  # Red to blue gradient
        # color_continuous_scale=['#123262', '#5cc8c6', '#f6d488', '#FFFFFF']  # Red to blue gradient
    )

    figure.update_layout(
        images=[dict(
            source='https://pbs.twimg.com/profile_images/1757761164556021760/WK-zxj8K_400x400.jpg',
            # Replace with the URL or local path of your image
            xref='paper', yref='paper',
            x=0.5, y=0.55,  # Positioning the image at the center
            sizex=0.18, sizey=0.18,  # Adjust size as needed
            xanchor='center', yanchor='middle',
            layer='above'  # Ensures the image is placed on top of the plot
        )],
    )

    figure.add_annotation(
        dict(
            font=dict(
                color='black',
                size=15
            ),
            xref='paper', yref='paper',
            x=0.5, y=0.43,  # Positioning the image at the center
            showarrow=False,
            text=f'{stars}<br>{total_score}/100',
            textangle=0,
            xanchor='center',
        )
    )

    figure.update_traces(
        hovertemplate='Score: %{value:.2f}'
    )

    figure.update_layout(
        margin=dict(
            t=0,
            l=0,
            r=0,
            b=0
        )
    )

    # Generate HTML div as a string
    html_div = pio.to_html(
        figure,
        default_width='100%',
        include_plotlyjs='cdn',
        full_html=False,
        config={'staticPlot': False}
    )

    return html_div


def plot_label_as_image(dataset: Dataset):
    elements = []
    parents = []
    values = []

    scores, total_score = compute_scores(dataset=dataset)

    stars = generate_assessment_stars(
        total_score,
        empty_star='\u2606',
        filled_star='\u2605'
    )

    total_score = '{:.2f}'.format(total_score)

    elements.append('QUANTUM')
    parents.append('')
    values.append(100)

    for category in EHDSCategory.objects.all():
        dimensions = DQDimension.objects.filter(ehds_category=category)

        elements.append(category.name)
        parents.append('QUANTUM')
        values.append(scores[category.name]['relevance'])

        for dimension in dimensions:
            elements.append(dimension.name)
            parents.append(category.name)

            if scores[category.name]['dimensions'][dimension.name]['score'] > 0:
                score = scores[category.name]['dimensions'][dimension.name]['score']
            else:
                score = 0
            values.append(score)

    data = dict(
        elements=elements,
        parents=parents,
        values=values
    )

    # Create the sunburst plot
    figure = px.sunburst(
        data,
        names='elements',
        parents='parents',
        values='values',
        title='',
        branchvalues='total',
    )

    figure.update_layout(
        images=[dict(
            source='https://pbs.twimg.com/profile_images/1757761164556021760/WK-zxj8K_400x400.jpg',
            xref='paper', yref='paper',
            x=0.5, y=0.55,
            sizex=0.18, sizey=0.18,
            xanchor='center', yanchor='middle',
            layer='above'
        )],
    )

    figure.add_annotation(
        dict(
            font=dict(
                color='black',
                size=15
            ),
            xref='paper', yref='paper',
            x=0.5, y=0.43,
            showarrow=False,
            text=f'{stars}<br>{total_score}/100',
            textangle=0,
            xanchor='center',
        )
    )

    figure.update_traces(
        hovertemplate='Score: %{value:.2f}'
    )

    figure.update_layout(
        margin=dict(
            t=0,
            l=0,
            r=0,
            b=0
        )
    )

    # Convert figure to image in memory (PNG)
    img_bytes = pio.to_image(figure, format="png")

    # Encode image to base64
    encoded_img = base64.b64encode(img_bytes).decode('utf-8')

    # Return the base64 string
    return f"data:image/png;base64,{encoded_img}"


def compute_scores(dataset: Dataset) -> [dict, float]:
    # Compute the assessment table
    dimensions_total_relevance = DQDimension.objects.aggregate(Sum('relevance'))['relevance__sum']

    results = {}
    total_score = 0
    assessment = dataset.dq_assessment
    ehds_categories = EHDSCategory.objects.all()
    for category in ehds_categories:
        results[category.name] = {
            'relevance': 0,
            'dimensions': {},
            'score': 0
        }

        dimensions = DQDimension.objects.filter(ehds_category=category)
        for dimension in dimensions:
            dimension_relevance = (dimension.relevance / dimensions_total_relevance)
            results[category.name]['dimensions'][dimension.name] = {
                'relevance': dimension_relevance,
                # this part take care of showing the number of stars in the dashboard (removed the *100 cause I increase the metrics weight by 100)
                'metrics': {},
                'score': 0
            }
            results[category.name]['relevance'] += (dimension_relevance * 100)

            metrics = DQMetric.objects.filter(dq_dimension=dimension)
            for metric_index, metric in enumerate(metrics):
                results[category.name]['dimensions'][dimension.name]['metrics'][metric.definition] = {
                    'weight': int(metric.weight),  # idk what this affects.
                    'score': 0
                }
                metric_score = 0

                dq_metric_value = DQMetricValue.objects.filter(dq_assessment=assessment, dq_metric=metric)
                current_value = None

                # If the metric is filled then we assign the value, else it is None
                if len(dq_metric_value) >= 1:
                    current_value = str(dq_metric_value.first().value)
                else:
                    pass

                # For the categorical metrics we provide the possible values
                if getattr(metric, 'dqcategoricalmetric') is not None and current_value:
                    current_value = int(current_value)
                    metric_categories = DQCategoricalMetricCategory.objects.filter(
                        dq_categorical_metric=metric
                    ).count()

                    metric_score = current_value / (metric_categories - 1)  # If 3 : 0, 1, 2 -> 0% 50% 100%
                metric_score = metric_score * metric.weight * results[category.name]['dimensions'][dimension.name][
                    'relevance']
                results[category.name]['dimensions'][dimension.name]['metrics'][metric.definition][
                    'score'] = metric_score
                results[category.name]['dimensions'][dimension.name]['score'] += metric_score
                results[category.name]['score'] += metric_score

            total_score += results[category.name]['dimensions'][dimension.name]['score']

    return results, total_score
