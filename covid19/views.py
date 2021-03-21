import decimal
import time
from math import pi

import pandas
from django.shortcuts import render

from datetime import datetime
import datetime
from .models import Covid19
from django.db.models import Q

from bokeh.embed import components
from bokeh.plotting import figure

import folium
import pandas as pd
import branca.colormap as cm
import geopandas as gpd
import numpy as np


def query(request):
    if request.GET.get("Location") and request.GET.get("start_date") and request.GET.get("end_date"):
        location_filter = request.GET.get("Location")

        start_date = request.GET.get("start_date")
        start_date_list = start_date.split("-")
        selected_start_date = datetime.datetime(int(start_date_list[0]), int(start_date_list[1]),
                                                int(start_date_list[2]))

        end_date = request.GET.get("end_date")
        end_date_list = end_date.split("-")
        selected_end_date = datetime.datetime(int(end_date_list[0]), int(end_date_list[1]), int(end_date_list[2]))
        query_result = Covid19.objects.filter(Q(location=location_filter) & Q(date__gte=selected_start_date)
                                              & Q(date__lte=selected_end_date))

        # Create a list to hold the dates that have been included
        date_list = []
        dayIncrement = datetime.timedelta(days=1)
        counter = 0

        # Find out the actual starting date in the database for that country
        while Covid19.objects.filter(Q(location=location_filter)
                                     & Q(date=selected_start_date)).exists() is False:
            selected_start_date += dayIncrement

        index = selected_start_date

        # Prepare date list
        while index <= selected_end_date:
            date_list.append(selected_start_date.isoformat())
            selected_start_date += dayIncrement
            index += dayIncrement
            counter += 1

        # Prepare data for the graphs
        cases_list = []
        deaths_list = []
        rep_list = []
        icu_list = []
        hosp_list = []
        i = 0
        j = 0
        k = 0
        l = 0
        m = 0
        print(counter)
        for cases in query_result.values_list('total_cases'):
            if i <= counter:
                cases_list.append(cases)
                i += 1

        for deaths in query_result.values_list('total_deaths'):
            if j <= counter:
                deaths_list.append(deaths)
                j += 1

        for rep in query_result.values_list('reproduction_rate'):
            if k <= counter:
                rep_list.append(rep)
                k += 1

        for icu in query_result.values_list('icu_patients'):
            if l <= counter:
                icu_list.append(icu)
                l += 1

        for hos in query_result.values_list('hosp_patients'):
            if m <= counter:
                hosp_list.append(hos)
                m += 1

        print(date_list[0].split("-"))

        # Reformat the dates for plotting
        graph_date_list = []
        for x in range(len(date_list)):
            reformatted_date_list = date_list[x].split("-")
            if reformatted_date_list[0] == "2020":
                if reformatted_date_list[1] == "01":
                    graph_date_list.append("2020/01")
                elif reformatted_date_list[1] == "02":
                    graph_date_list.append("2020/02")
                elif reformatted_date_list[1] == "03":
                    graph_date_list.append("2020/03")
                elif reformatted_date_list[1] == "04":
                    graph_date_list.append("2020/04")
                elif reformatted_date_list[1] == "05":
                    graph_date_list.append("2020/05")
                elif reformatted_date_list[1] == "06":
                    graph_date_list.append("2020/06")
                elif reformatted_date_list[1] == "07":
                    graph_date_list.append("2020/07")
                elif reformatted_date_list[1] == "08":
                    graph_date_list.append("2020/08")
                elif reformatted_date_list[1] == "09":
                    graph_date_list.append("2020/09")
                elif reformatted_date_list[1] == "10":
                    graph_date_list.append("2020/10")
                elif reformatted_date_list[1] == "11":
                    graph_date_list.append("2020/11")
                elif reformatted_date_list[1] == "12":
                    graph_date_list.append("2020/12")

            else:
                if reformatted_date_list[1] == "01":
                    graph_date_list.append("2021/01")
                elif reformatted_date_list[1] == "02":
                    graph_date_list.append("2021/02")
                elif reformatted_date_list[1] == "03":
                    graph_date_list.append("2021/03")
                elif reformatted_date_list[1] == "04":
                    graph_date_list.append("2021/04")
                elif reformatted_date_list[1] == "05":
                    graph_date_list.append("2021/05")
                elif reformatted_date_list[1] == "06":
                    graph_date_list.append("2021/06")
                elif reformatted_date_list[1] == "07":
                    graph_date_list.append("2021/07")
                elif reformatted_date_list[1] == "08":
                    graph_date_list.append("2021/08")
                elif reformatted_date_list[1] == "09":
                    graph_date_list.append("2021/09")
                elif reformatted_date_list[1] == "10":
                    graph_date_list.append("2021/10")
                elif reformatted_date_list[1] == "11":
                    graph_date_list.append("2021/11")
                elif reformatted_date_list[1] == "12":
                    graph_date_list.append("2021/12")

        # Plot the graph of total cases
        month_list = ["2020/01", "2020/02", "2020/03", "2020/04", "2020/05", "2020/06", "2020/07",
                      "2020/08", "2020/09", "2020/10", "2020/11", "2020/12",
                      "2021/01", "2021/02", "2021/03", "2021/04"]
        plot2 = figure(title="Number of Total cases from " + start_date + " to " + end_date,
                       x_range=month_list,
                       plot_width=1000,
                       plot_height=400)

        plot2.vbar(graph_date_list, width=0.5, bottom=0, top=cases_list, color="firebrick")
        plot2.left[0].formatter.use_scientific = False

        # plot2.line(graph_date_list, cases_list, line_width=2)
        script2, div2 = components(plot2)

        # Plot the number of total deaths
        plot3 = figure(title="Number of Total Deaths from " + start_date + " to " + end_date,
                       x_range=month_list,
                       plot_width=800, plot_height=400)
        plot3.left[0].formatter.use_scientific = False
        # lot3.line(graph_date_list, deaths_list, line_width=2)
        plot3.vbar(graph_date_list, width=0.5, bottom=0, top=deaths_list, color="firebrick")
        script3, div3 = components(plot3)

        # Plot reproduction Rate of covid 19
        plot4 = figure(title="Reproduction Rate of COVID 19 from " + start_date + " to " + end_date,
                       x_range=month_list,
                       plot_width=800, plot_height=400)
        plot4.left[0].formatter.use_scientific = False
        # lot3.line(graph_date_list, deaths_list, line_width=2)
        plot4.vbar(graph_date_list, width=0.5, bottom=0, top=rep_list, color="firebrick")
        script4, div4 = components(plot4)

        # Plot number of COVID 19 patients admitted into ICU
        plot5 = figure(title="Number of COVID 19 Patients Admitted into ICU from " + start_date + " to " + end_date,
                       x_range=month_list,
                       plot_width=800, plot_height=400)
        plot5.left[0].formatter.use_scientific = False
        # lot3.line(graph_date_list, deaths_list, line_width=2)
        plot5.vbar(graph_date_list, width=0.5, bottom=0, top=rep_list, color="firebrick")
        script5, div5 = components(plot5)

        # Plot number of COVID 19 patients admitted into hospitals
        plot6 = figure(
            title="Number of COVID 19 Patients Admitted into hospitals from " + start_date + " to " + end_date,
            x_range=month_list,
            plot_width=800, plot_height=400)
        plot6.left[0].formatter.use_scientific = False
        # lot3.line(graph_date_list, deaths_list, line_width=2)
        plot6.vbar(graph_date_list, width=0.5, bottom=0, top=rep_list, color="firebrick")
        script6, div6 = components(plot6)

        context = {'Covid19': query_result, 'script2': script2, 'div2': div2, 'script3': script3, 'div3': div3,
                   'script4': script4, 'div4': div4, 'script5': script5, 'div5': div5,
                   'script6': script6, 'div6': div6}
        return render(request, 'covid19/query.html', context)

    return render(request, 'covid19/query.html')


def about(request):
    return render(request, 'covid19/about.html')


def covid19_map(request):
    return render(request, 'covid19/covid19_map.html')


def covid19_day_stat(request):
    return render(request, 'covid19/covid19_day_stat.html')


def covid19_day_stat_map(request):
    if (request.GET.get("Location") != "World") and request.GET.get("start_date"):
        location_filter = request.GET.get("Location")
        start_date = request.GET.get("start_date")
        query_result = Covid19.objects.filter(Q(location=location_filter) & Q(date=start_date))

        cases_list = []
        deaths_list = []
        rep_list = []
        icu_list = []
        hosp_list = []
        lat_list = []
        lon_list = []
        name_list = []

        for q in query_result:
            lat_list.append(q.Latitude)
            lon_list.append(q.Longitude)
            name_list.append(q.location)
            cases_list.append(q.total_cases)
            deaths_list.append(q.total_deaths)
            rep_list.append(q.reproduction_rate)
            icu_list.append(q.icu_patients)
            hosp_list.append(q.hosp_patients)

        combined = zip(cases_list, deaths_list, rep_list, icu_list, hosp_list, lat_list, lon_list, name_list)
        zipped_combined = list(combined)

        map_demo = folium.Map(min_zoom=2, max_bounds=True, tiles='cartodbpositron')

        for co in zipped_combined:
            html = """Country: """ + co[7] \
                   + """<br>Date: """ + start_date \
                   + """<br>Case Number: """ + str(co[0]) \
                   + """<br>Deaths on: """ + str(co[1]) \
                   + """<br>Reproduction rate: """ + str(co[2]) \
                   + """<br>Number of ICU patients: """ + str(co[3]) \
                   + """<br>Number of hospitalized patients: """ + str(co[4])

            iframe = folium.IFrame(html,
                                   width=400,
                                   height=200)

            popup = folium.Popup(iframe,
                                 max_width=500)
            folium.Marker(location=[co[5], co[6]], popup=popup).add_to(map_demo)

        map_demo.save("covid19/covid19_day_stat_map.html")
        map_demo = map_demo._repr_html_()
        context = {
            'map_demo': map_demo
        }

        return render(request, 'covid19/covid19_day_stat_map.html', context)

    elif (request.GET.get("Location") == "World") and request.GET.get("start_date"):
        start_date = request.GET.get("start_date")
        query_result = Covid19.objects.filter(date=start_date)

        query_result = query_result.exclude(location="World").exclude(location="North America").exclude(
            location="European Union").exclude(location="Asia").exclude(location="South America").exclude(
            location="Oceania").exclude(location="Africa").exclude(location="Georgia").exclude(location="Chad").exclude(
            location="Jordan")

        cases_list = []
        deaths_list = []
        rep_list = []
        icu_list = []
        hosp_list = []
        lat_list = []
        lon_list = []
        name_list = []

        for q in query_result:
            lat_list.append(q.Latitude)
            lon_list.append(q.Longitude)
            name_list.append(q.location)
            cases_list.append(q.total_cases)
            deaths_list.append(q.total_deaths)
            rep_list.append(q.reproduction_rate)
            icu_list.append(q.icu_patients)
            hosp_list.append(q.hosp_patients)

        combined = zip(cases_list, deaths_list, rep_list, icu_list, hosp_list, lat_list, lon_list, name_list)
        zipped_combined = list(combined)
        featured_Group = folium.FeatureGroup(name="COVID 19 Map")
        map_demo = folium.Map(min_zoom=2, max_bounds=True, tiles='cartodbpositron')

        for co in zipped_combined:
            html = """Country: """ + co[7] \
                   + """<br>Date: """ + start_date \
                   + """<br>Case Number: """ + str(co[0]) \
                   + """<br>Deaths on: """ + str(co[1]) \
                   + """<br>Reproduction rate: """ + str(co[2]) \
                   + """<br>Number of ICU patients: """ + str(co[3]) \
                   + """<br>Number of hospitalized patients: """ + str(co[4])

            iframe = folium.IFrame(html,
                                   width=400,
                                   height=200)

            popup = folium.Popup(iframe,
                                 max_width=500)
            # folium.Marker(location=[co[5], co[6]], popup=popup).add_to(map_demo)
            featured_Group.add_child(folium.Marker(location=[co[5], co[6]], popup=popup))
        map_demo.add_child(featured_Group)

        map_demo.save("covid19/covid19_day_stat_map.html")
        map_demo = map_demo._repr_html_()
        context = {
            'map_demo': map_demo
        }

        return render(request, 'covid19/covid19_day_stat_map.html', context)

    return render(request, 'covid19/covid19_day_stat_map.html')


def covid19_cum_stat(request):
    return render(request, 'covid19/covid19_cum_stat.html')


def covid19_cum_stat_map(request):
    obtained_feature = request.GET.get("feature")
    date = request.GET.get("start_date")
    slider_name_list = []
    slider_case_list = []
    slider_death_list = []
    slider_lat_list = []
    slider_lon_list = []
    slider_date_list = []
    slider_rep_list = []
    slider_icu_list = []
    slider_hosp_list = []

    if obtained_feature == "total_cases":
        result = Covid19.objects.filter(date__gte=date)
        result = result.exclude(location="World").exclude(location="North America").exclude(
            location="European Union").exclude(location="Asia").exclude(location="South America").exclude(
            location="Oceania").exclude(location="Africa").exclude(location="Georgia").exclude(location="Chad").exclude(
            location="Jordan")
        for m in result:
            slider_name_list.append(m.location)
            slider_case_list.append(m.total_cases)
            slider_lat_list.append(m.Latitude)
            slider_lon_list.append(m.Longitude)
            slider_date_list.append(m.date)

        combined = zip(slider_name_list, slider_case_list, slider_date_list)
        slider_combined = list(combined)
        df_slider = pd.DataFrame(data=slider_combined, columns=['location', 'total_cases', 'date'])
        df_slider = df_slider[df_slider.total_cases != 0]

        # sorting
        sorted_df = df_slider.sort_values(['location',
                                           'date']).reset_index(drop=True)

        # Combine data with the file
        country = gpd.read_file("/Users/benchiang/Desktop/countries.geojson")

        # Change country name
        country = country.replace({'ADMIN': 'United States of America'},
                                  'United States')
        country = country.rename(columns={'ADMIN': 'location'})
        combined_df = sorted_df.merge(country, on='location')

        # Use Log to plot the cases
        combined_df['log_total_cases'] = np.log10(combined_df['total_cases'])
        combined_df = combined_df[['location', 'log_total_cases', 'date', 'geometry']]

        combined_df['date'] = pd.to_datetime(combined_df['date']).astype(int) / 10 ** 9
        combined_df['date'] = combined_df['date'].astype(int).astype(str)

        # Construct color map
        max_color = max(combined_df['log_total_cases'])
        min_color = min(combined_df['log_total_cases'])
        color_map = cm.linear.YlOrRd_09.scale(min_color, max_color)
        combined_df['color'] = combined_df['log_total_cases'].map(color_map)

        # Construct style dictionary
        unique_country_list = combined_df['location'].unique().tolist()
        ctry_index = range(len(unique_country_list))

        style_dic = {}
        for j in ctry_index:
            ctry = unique_country_list[j]
            country = combined_df[combined_df['location'] == ctry]
            in_dic = {

            }
            for _, r in country.iterrows():
                in_dic[r['date']] = {'color': r['color'], 'opacity': 0.8}
            style_dic[str(j)] = in_dic

        # Make a dataframe containing each country
        specific_ctry = combined_df[['geometry']]
        ctry_gdf = gpd.GeoDataFrame(specific_ctry)
        ctry_gdf = ctry_gdf.drop_duplicates().reset_index()

        # Create a slider map
        from folium.plugins import TimeSliderChoropleth
        m = folium.Map(min_zoom=2, max_bounds=True, tiles='cartodbpositron')

        # Plot Slider Map
        _ = TimeSliderChoropleth(
            data=ctry_gdf.to_json(),
            styledict=style_dic,
        ).add_to(m)
        _ = color_map.add_to(m)
        color_map.caption = "Log number of COVID 19 cases"

        m.save("covid19/covid19_cum_stat_map.html")
        m = m._repr_html_()
        context = {
            'm': m
        }

        return render(request, 'covid19/covid19_cum_stat_map.html', context)
    elif obtained_feature == "total_deaths":
        result = Covid19.objects.filter(date__gte=date)
        result = result.exclude(location="World").exclude(location="North America").exclude(
            location="European Union").exclude(location="Asia").exclude(location="South America").exclude(
            location="Oceania").exclude(location="Africa").exclude(location="Georgia").exclude(location="Chad").exclude(
            location="Jordan")
        for m in result:
            slider_name_list.append(m.location)
            slider_death_list.append(m.total_deaths)
            slider_lat_list.append(m.Latitude)
            slider_lon_list.append(m.Longitude)
            slider_date_list.append(m.date)

        combined = zip(slider_name_list, slider_death_list, slider_date_list)
        slider_combined = list(combined)
        df_slider = pd.DataFrame(data=slider_combined, columns=['location', 'total_deaths', 'date'])
        df_slider = df_slider[df_slider.total_deaths != 0]

        # sorting
        sorted_df = df_slider.sort_values(['location',
                                           'date']).reset_index(drop=True)

        # Combine data with the file
        country = gpd.read_file("/Users/benchiang/Desktop/countries.geojson")

        # Change country name
        country = country.replace({'ADMIN': 'United States of America'},
                                  'United States')
        country = country.rename(columns={'ADMIN': 'location'})
        combined_df = sorted_df.merge(country, on='location')

        # Use Log to plot the cases
        # combined_df['log_total_cases'] = np.log10(combined_df['total_deaths'])
        combined_df = combined_df[['location', 'total_deaths', 'date', 'geometry']]

        combined_df['date'] = pd.to_datetime(combined_df['date']).astype(int) / 10 ** 9
        combined_df['date'] = combined_df['date'].astype(int).astype(str)

        # Construct color map
        max_color = max(combined_df['total_deaths'])
        min_color = min(combined_df['total_deaths'])
        color_map = cm.linear.YlOrRd_09.scale(min_color, max_color)
        combined_df['color'] = combined_df['total_deaths'].map(color_map)

        # Construct style dictionary
        unique_country_list = combined_df['location'].unique().tolist()
        ctry_index = range(len(unique_country_list))

        style_dic = {}
        for j in ctry_index:
            ctry = unique_country_list[j]
            country = combined_df[combined_df['location'] == ctry]
            in_dic = {

            }
            for _, r in country.iterrows():
                in_dic[r['date']] = {'color': r['color'], 'opacity': 0.8}
            style_dic[str(j)] = in_dic

        # Make a dataframe containing each country
        specific_ctry = combined_df[['geometry']]
        ctry_gdf = gpd.GeoDataFrame(specific_ctry)
        ctry_gdf = ctry_gdf.drop_duplicates().reset_index()

        # Create a slider map
        from folium.plugins import TimeSliderChoropleth
        m = folium.Map(min_zoom=2, max_bounds=True, tiles='cartodbpositron')

        # Plot Slider Map
        _ = TimeSliderChoropleth(
            data=ctry_gdf.to_json(),
            styledict=style_dic,
        ).add_to(m)
        _ = color_map.add_to(m)
        color_map.caption = "Number of COVID 19 deaths"

        m.save("covid19/covid19_cum_stat_map.html")
        m = m._repr_html_()
        context = {
            'm': m
        }
        return render(request, 'covid19/covid19_cum_stat_map.html', context)
    elif obtained_feature == "reproduction_rate":
        result = Covid19.objects.filter(date__gte=date)
        result = result.exclude(location="World").exclude(location="North America").exclude(
            location="European Union").exclude(location="Asia").exclude(location="South America").exclude(
            location="Oceania").exclude(location="Africa").exclude(location="Georgia").exclude(location="Chad").exclude(
            location="Jordan")
        for m in result:
            slider_name_list.append(m.location)
            slider_rep_list.append(m.reproduction_rate)
            slider_lat_list.append(m.Latitude)
            slider_lon_list.append(m.Longitude)
            slider_date_list.append(m.date)

        combined = zip(slider_name_list, slider_rep_list, slider_date_list)
        slider_combined = list(combined)
        df_slider = pd.DataFrame(data=slider_combined, columns=['location', 'reproduction_rate', 'date'])
        df_slider = df_slider[df_slider.reproduction_rate != 0]

        # sorting
        sorted_df = df_slider.sort_values(['location',
                                           'date']).reset_index(drop=True)

        # Combine data with the file
        country = gpd.read_file("/Users/benchiang/Desktop/countries.geojson")

        # Change country name
        country = country.replace({'ADMIN': 'United States of America'},
                                  'United States')
        country = country.rename(columns={'ADMIN': 'location'})
        combined_df = sorted_df.merge(country, on='location')

        # Use Log to plot the cases
        # combined_df['log_total_cases'] = np.log10(combined_df['total_deaths'])
        combined_df = combined_df[['location', 'reproduction_rate', 'date', 'geometry']]

        combined_df['date'] = pd.to_datetime(combined_df['date']).astype(int) / 10 ** 9
        combined_df['date'] = combined_df['date'].astype(int).astype(str)

        # Construct color map
        combined_df['reproduction_rate'] = np.multiply(combined_df['reproduction_rate'], 100).astype(int)
        max_color = max(combined_df['reproduction_rate'])
        min_color = min(combined_df['reproduction_rate'])
        color_map = cm.linear.YlOrRd_09.scale(min_color, max_color)
        combined_df['color'] = combined_df['reproduction_rate'].map(color_map)

        # Construct style dictionary
        unique_country_list = combined_df['location'].unique().tolist()
        ctry_index = range(len(unique_country_list))

        style_dic = {}
        for j in ctry_index:
            ctry = unique_country_list[j]
            country = combined_df[combined_df['location'] == ctry]
            in_dic = {

            }
            for _, r in country.iterrows():
                in_dic[r['date']] = {'color': r['color'], 'opacity': 0.8}
            style_dic[str(j)] = in_dic

        # Make a dataframe containing each country
        specific_ctry = combined_df[['geometry']]
        ctry_gdf = gpd.GeoDataFrame(specific_ctry)
        ctry_gdf = ctry_gdf.drop_duplicates().reset_index()

        # Create a slider map
        from folium.plugins import TimeSliderChoropleth
        m = folium.Map(min_zoom=2, max_bounds=True, tiles='cartodbpositron')

        # Plot Slider Map
        _ = TimeSliderChoropleth(
            data=ctry_gdf.to_json(),
            styledict=style_dic,
        ).add_to(m)
        _ = color_map.add_to(m)
        color_map.caption = "COVID 19 Reproduction Rate"

        m.save("covid19/covid19_cum_stat_map.html")
        m = m._repr_html_()
        context = {
            'm': m
        }
        return render(request, 'covid19/covid19_cum_stat_map.html', context)
    elif obtained_feature == "icu_patients":
        result = Covid19.objects.filter(date__gte=date)
        result = result.exclude(location="World").exclude(location="North America").exclude(
            location="European Union").exclude(location="Asia").exclude(location="South America").exclude(
            location="Oceania").exclude(location="Africa").exclude(location="Georgia").exclude(location="Chad").exclude(
            location="Jordan")
        for m in result:
            slider_name_list.append(m.location)
            slider_icu_list.append(m.icu_patients)
            slider_lat_list.append(m.Latitude)
            slider_lon_list.append(m.Longitude)
            slider_date_list.append(m.date)

        combined = zip(slider_name_list, slider_icu_list, slider_date_list)
        slider_combined = list(combined)
        df_slider = pd.DataFrame(data=slider_combined, columns=['location', 'icu_patients', 'date'])
        df_slider = df_slider[df_slider.icu_patients != 0]

        # sorting
        sorted_df = df_slider.sort_values(['location',
                                           'date']).reset_index(drop=True)

        # Combine data with the file
        country = gpd.read_file("/Users/benchiang/Desktop/countries.geojson")

        # Change country name
        country = country.replace({'ADMIN': 'United States of America'},
                                  'United States')
        country = country.rename(columns={'ADMIN': 'location'})
        combined_df = sorted_df.merge(country, on='location')

        # Use Log to plot the cases
        # combined_df['log_total_cases'] = np.log10(combined_df['total_deaths'])
        combined_df = combined_df[['location', 'icu_patients', 'date', 'geometry']]

        combined_df['date'] = pd.to_datetime(combined_df['date']).astype(int) / 10 ** 9
        combined_df['date'] = combined_df['date'].astype(int).astype(str)

        # Construct color map
        max_color = max(combined_df['icu_patients'])
        min_color = min(combined_df['icu_patients'])
        color_map = cm.linear.YlOrRd_09.scale(min_color, max_color)
        combined_df['color'] = combined_df['icu_patients'].map(color_map)

        # Construct style dictionary
        unique_country_list = combined_df['location'].unique().tolist()
        ctry_index = range(len(unique_country_list))

        style_dic = {}
        for j in ctry_index:
            ctry = unique_country_list[j]
            country = combined_df[combined_df['location'] == ctry]
            in_dic = {

            }
            for _, r in country.iterrows():
                in_dic[r['date']] = {'color': r['color'], 'opacity': 0.8}
            style_dic[str(j)] = in_dic

        # Make a dataframe containing each country
        specific_ctry = combined_df[['geometry']]
        ctry_gdf = gpd.GeoDataFrame(specific_ctry)
        ctry_gdf = ctry_gdf.drop_duplicates().reset_index()

        # Create a slider map
        from folium.plugins import TimeSliderChoropleth
        m = folium.Map(min_zoom=2, max_bounds=True, tiles='cartodbpositron')

        # Plot Slider Map
        _ = TimeSliderChoropleth(
            data=ctry_gdf.to_json(),
            styledict=style_dic,
        ).add_to(m)
        _ = color_map.add_to(m)
        color_map.caption = "Number of COVID 19 patients admitted into ICU"

        m.save("covid19/covid19_cum_stat_map.html")
        m = m._repr_html_()
        context = {
            'm': m
        }
        return render(request, 'covid19/covid19_cum_stat_map.html', context)
    elif obtained_feature == "hosp_patients":
        result = Covid19.objects.filter(date__gte=date)
        result = result.exclude(location="World").exclude(location="North America").exclude(
            location="European Union").exclude(location="Asia").exclude(location="South America").exclude(
            location="Oceania").exclude(location="Africa").exclude(location="Georgia").exclude(location="Chad").exclude(
            location="Jordan")
        for m in result:
            slider_name_list.append(m.location)
            slider_hosp_list.append(m.hosp_patients)
            slider_lat_list.append(m.Latitude)
            slider_lon_list.append(m.Longitude)
            slider_date_list.append(m.date)

        combined = zip(slider_name_list, slider_hosp_list, slider_date_list)
        slider_combined = list(combined)
        df_slider = pd.DataFrame(data=slider_combined, columns=['location', 'hosp_patients', 'date'])
        df_slider = df_slider[df_slider.hosp_patients != 0]

        # sorting
        sorted_df = df_slider.sort_values(['location',
                                           'date']).reset_index(drop=True)

        # Combine data with the file
        country = gpd.read_file("/Users/benchiang/Desktop/countries.geojson")

        # Change country name
        country = country.replace({'ADMIN': 'United States of America'},
                                  'United States')
        country = country.rename(columns={'ADMIN': 'location'})
        combined_df = sorted_df.merge(country, on='location')

        # Use Log to plot the cases
        # combined_df['log_total_cases'] = np.log10(combined_df['total_deaths'])
        combined_df = combined_df[['location', 'hosp_patients', 'date', 'geometry']]

        combined_df['date'] = pd.to_datetime(combined_df['date']).astype(int) / 10 ** 9
        combined_df['date'] = combined_df['date'].astype(int).astype(str)

        # Construct color map
        max_color = max(combined_df['hosp_patients'])
        min_color = min(combined_df['hosp_patients'])
        color_map = cm.linear.YlOrRd_09.scale(min_color, max_color)
        combined_df['color'] = combined_df['hosp_patients'].map(color_map)

        # Construct style dictionary
        unique_country_list = combined_df['location'].unique().tolist()
        ctry_index = range(len(unique_country_list))

        style_dic = {}
        for j in ctry_index:
            ctry = unique_country_list[j]
            country = combined_df[combined_df['location'] == ctry]
            in_dic = {

            }
            for _, r in country.iterrows():
                in_dic[r['date']] = {'color': r['color'], 'opacity': 0.8}
            style_dic[str(j)] = in_dic

        # Make a dataframe containing each country
        specific_ctry = combined_df[['geometry']]
        ctry_gdf = gpd.GeoDataFrame(specific_ctry)
        ctry_gdf = ctry_gdf.drop_duplicates().reset_index()

        # Create a slider map
        from folium.plugins import TimeSliderChoropleth
        m = folium.Map(min_zoom=2, max_bounds=True, tiles='cartodbpositron')

        # Plot Slider Map
        _ = TimeSliderChoropleth(
            data=ctry_gdf.to_json(),
            styledict=style_dic,
        ).add_to(m)
        _ = color_map.add_to(m)
        color_map.caption = "Number of COVID 19 patients admitted into hospitals"

        m.save("covid19/covid19_cum_stat_map.html")
        m = m._repr_html_()
        context = {
            'm': m
        }
        return render(request, 'covid19/covid19_cum_stat_map.html', context)

    return render(request, 'covid19/covid19_cum_stat_map.html')


def covid19_public_health_authority_response(request):
    return render(request, 'covid19/covid19_public_health_authority_response.html')


def covid19_public_health_test_stat(request):
    if request.GET.get("Location") and request.GET.get("start_date") and request.GET.get("end_date"):
        country_filter = request.GET.get("Location")
        date_filter = request.GET.get("start_date")
        end_date_filter = request.GET.get("end_date")
        processed_date_list = date_filter.split("-")
        end_processed_date_list = end_date_filter.split("-")
        date_ready = datetime.datetime(int(processed_date_list[0]), int(processed_date_list[1]),
                                       int(processed_date_list[2]))
        end_date_ready = datetime.datetime(int(end_processed_date_list[0]), int(end_processed_date_list[1]),
                                           int(end_processed_date_list[2]))
        query_result = Covid19.objects.filter(Q(location=country_filter) & Q(date__gte=date_filter))

        cases_list = []
        test_list = []
        name_list = []

        # Create a list to hold the dates that have been included
        date_list = []
        dayIncrement = datetime.timedelta(days=1)
        counter = 0

        # Find out the actual starting date in the database for that country
        while Covid19.objects.filter(Q(location=country_filter)
                                     & Q(date=date_ready)).exists() is False:
            date_ready += dayIncrement

        index = date_ready

        # Prepare date list
        while index <= end_date_ready:
            date_list.append(date_ready.isoformat())
            date_ready += dayIncrement
            index += dayIncrement
            counter += 1

        # Prepare tests and cases stats
        i = 0
        j = 0
        for cases in query_result.values_list('total_cases'):
            if i <= counter:
                cases_list.append(cases)
                i += 1

        for test in query_result.values_list('total_tests'):
            if j <= counter:
                test_list.append(test)
                j += 1

        # Reformat the dates for plotting
        graph_date_list = []
        for x in range(len(date_list)):
            reformatted_date_list = date_list[x].split("-")
            if reformatted_date_list[0] == "2020":
                if reformatted_date_list[1] == "01":
                    graph_date_list.append("2020/01")
                elif reformatted_date_list[1] == "02":
                    graph_date_list.append("2020/02")
                elif reformatted_date_list[1] == "03":
                    graph_date_list.append("2020/03")
                elif reformatted_date_list[1] == "04":
                    graph_date_list.append("2020/04")
                elif reformatted_date_list[1] == "05":
                    graph_date_list.append("2020/05")
                elif reformatted_date_list[1] == "06":
                    graph_date_list.append("2020/06")
                elif reformatted_date_list[1] == "07":
                    graph_date_list.append("2020/07")
                elif reformatted_date_list[1] == "08":
                    graph_date_list.append("2020/08")
                elif reformatted_date_list[1] == "09":
                    graph_date_list.append("2020/09")
                elif reformatted_date_list[1] == "10":
                    graph_date_list.append("2020/10")
                elif reformatted_date_list[1] == "11":
                    graph_date_list.append("2020/11")
                elif reformatted_date_list[1] == "12":
                    graph_date_list.append("2020/12")

            else:
                if reformatted_date_list[1] == "01":
                    graph_date_list.append("2021/01")
                elif reformatted_date_list[1] == "02":
                    graph_date_list.append("2021/02")
                elif reformatted_date_list[1] == "03":
                    graph_date_list.append("2021/03")
                elif reformatted_date_list[1] == "04":
                    graph_date_list.append("2021/04")
                elif reformatted_date_list[1] == "05":
                    graph_date_list.append("2021/05")
                elif reformatted_date_list[1] == "06":
                    graph_date_list.append("2021/06")
                elif reformatted_date_list[1] == "07":
                    graph_date_list.append("2021/07")
                elif reformatted_date_list[1] == "08":
                    graph_date_list.append("2021/08")
                elif reformatted_date_list[1] == "09":
                    graph_date_list.append("2021/09")
                elif reformatted_date_list[1] == "10":
                    graph_date_list.append("2021/10")
                elif reformatted_date_list[1] == "11":
                    graph_date_list.append("2021/11")
                elif reformatted_date_list[1] == "12":
                    graph_date_list.append("2021/12")

        # Plot the graph of total cases
        month_list = ["2020/01", "2020/02", "2020/03", "2020/04", "2020/05", "2020/06", "2020/07",
                      "2020/08", "2020/09", "2020/10", "2020/11", "2020/12",
                      "2021/01", "2021/02", "2021/03", "2021/04"]
        plot2 = figure(title="Number of Total cases from " + date_filter + " to " + end_date_filter,
                       x_range=month_list,
                       plot_width=1000,
                       plot_height=400)

        plot2.vbar(graph_date_list, width=0.5, bottom=0, top=cases_list, color="firebrick")
        plot2.left[0].formatter.use_scientific = False
        script2, div2 = components(plot2)

        # Plot the graph of total tests
        plot3 = figure(title="Number of Total tests from " + date_filter + " to " + end_date_filter,
                       x_range=month_list,
                       plot_width=1000,
                       plot_height=400)
        plot3.vbar(graph_date_list, width=0.5, bottom=0, top=test_list, color="firebrick")
        plot3.left[0].formatter.use_scientific = False
        script3, div3 = components(plot3)

        # Plot the scatter plot for number of cases vs tests
        x_scatter_test = test_list
        y_scatter_case = cases_list

        scatter_plot_1 = figure(plot_width=700, plot_height=700, x_axis_label='Number of COVID 19 Tests',
                                y_axis_label='Number of COVID 19 Cases in ' + country_filter)
        scatter_plot_1.circle(x_scatter_test, y_scatter_case, size=10, line_color="navy", fill_color="orange",
                              fill_alpha=0.5)
        scatter_plot_1.left[0].formatter.use_scientific = False
        scatter_plot_1.below[0].formatter.use_scientific = False

        # Best-fit Line for population at risk vs gdp
        d = pandas.DataFrame(x_scatter_test)
        d1 = pandas.DataFrame(y_scatter_case)
        x = np.array(d[0])
        y = np.array(d1[0])

        par = np.polyfit(x, y, 1, full=True)
        slope = par[0][0]
        intercept = par[0][1]
        y_predicted_pop = [slope * i + intercept for i in x]
        scatter_plot_1.line(x, y_predicted_pop, color='red')
        script_test_case, div_test_case = components(scatter_plot_1)

        context = {'Covid19': query_result, 'script2': script2, 'div2': div2, 'script3': script3, 'div3': div3,
                   'script_test_case': script_test_case, 'div_test_case': div_test_case}

        return render(request, 'covid19/covid19_public_health_test_stat.html', context)

    return render(request, 'covid19/covid19_public_health_test_stat.html')


def covid19_public_health_vac_stat(request):
    if request.GET.get("Location") and request.GET.get("start_date") and request.GET.get("end_date"):
        country_filter = request.GET.get("Location")
        date_filter = request.GET.get("start_date")
        end_date_filter = request.GET.get("end_date")
        processed_date_list = date_filter.split("-")
        end_processed_date_list = end_date_filter.split("-")
        date_ready = datetime.datetime(int(processed_date_list[0]), int(processed_date_list[1]),
                                       int(processed_date_list[2]))
        end_date_ready = datetime.datetime(int(end_processed_date_list[0]), int(end_processed_date_list[1]),
                                           int(end_processed_date_list[2]))
        query_result = Covid19.objects.filter(Q(location=country_filter) & Q(date__gte=date_filter))

        cases_list = []
        deaths_list = []
        vac_pop_list = []
        vac_list = []
        name_list = []

        # Create a list to hold the dates that have been included
        date_list = []
        dayIncrement = datetime.timedelta(days=1)
        counter = 0

        # Find out the actual starting date in the database for that country
        while Covid19.objects.filter(Q(location=country_filter)
                                     & Q(date=date_ready)).exists() is False:
            date_ready += dayIncrement

        index = date_ready

        # Prepare date list
        while index <= end_date_ready:
            date_list.append(date_ready.isoformat())
            date_ready += dayIncrement
            index += dayIncrement
            counter += 1

        # Prepare tests and cases stats
        i = 0
        j = 0
        k = 0
        l = 0
        for cases in query_result.values_list('total_cases'):
            if i <= counter:
                cases_list.append(cases)
                i += 1

        for death in query_result.values_list('total_deaths'):
            if j <= counter:
                deaths_list.append(death)
                j += 1

        for vac_pop in query_result.values_list('people_vaccinated'):
            if k <= counter:
                vac_pop_list.append(vac_pop)

        for vac in query_result.values_list('total_vaccinations'):
            if l <= counter:
                vac_list.append(vac)

        # Reformat the dates for plotting
        graph_date_list = []
        for x in range(len(date_list)):
            reformatted_date_list = date_list[x].split("-")
            if reformatted_date_list[0] == "2020":
                if reformatted_date_list[1] == "01":
                    graph_date_list.append("2020/01")
                elif reformatted_date_list[1] == "02":
                    graph_date_list.append("2020/02")
                elif reformatted_date_list[1] == "03":
                    graph_date_list.append("2020/03")
                elif reformatted_date_list[1] == "04":
                    graph_date_list.append("2020/04")
                elif reformatted_date_list[1] == "05":
                    graph_date_list.append("2020/05")
                elif reformatted_date_list[1] == "06":
                    graph_date_list.append("2020/06")
                elif reformatted_date_list[1] == "07":
                    graph_date_list.append("2020/07")
                elif reformatted_date_list[1] == "08":
                    graph_date_list.append("2020/08")
                elif reformatted_date_list[1] == "09":
                    graph_date_list.append("2020/09")
                elif reformatted_date_list[1] == "10":
                    graph_date_list.append("2020/10")
                elif reformatted_date_list[1] == "11":
                    graph_date_list.append("2020/11")
                elif reformatted_date_list[1] == "12":
                    graph_date_list.append("2020/12")

            else:
                if reformatted_date_list[1] == "01":
                    graph_date_list.append("2021/01")
                elif reformatted_date_list[1] == "02":
                    graph_date_list.append("2021/02")
                elif reformatted_date_list[1] == "03":
                    graph_date_list.append("2021/03")
                elif reformatted_date_list[1] == "04":
                    graph_date_list.append("2021/04")
                elif reformatted_date_list[1] == "05":
                    graph_date_list.append("2021/05")
                elif reformatted_date_list[1] == "06":
                    graph_date_list.append("2021/06")
                elif reformatted_date_list[1] == "07":
                    graph_date_list.append("2021/07")
                elif reformatted_date_list[1] == "08":
                    graph_date_list.append("2021/08")
                elif reformatted_date_list[1] == "09":
                    graph_date_list.append("2021/09")
                elif reformatted_date_list[1] == "10":
                    graph_date_list.append("2021/10")
                elif reformatted_date_list[1] == "11":
                    graph_date_list.append("2021/11")
                elif reformatted_date_list[1] == "12":
                    graph_date_list.append("2021/12")

        month_list = ["2020/01", "2020/02", "2020/03", "2020/04", "2020/05", "2020/06", "2020/07",
                      "2020/08", "2020/09", "2020/10", "2020/11", "2020/12",
                      "2021/01", "2021/02", "2021/03", "2021/04"]

        # Plot the graph of number of people vaccinated
        plot3 = figure(
            title="Number of people vaccinated from " + date_filter + " to " + end_date_filter + " in " + country_filter,
            x_range=month_list,
            plot_width=1000,
            plot_height=400)
        plot3.vbar(graph_date_list, width=0.5, bottom=0, top=vac_pop_list, color="firebrick")
        plot3.left[0].formatter.use_scientific = False
        script3, div3 = components(plot3)

        # Plot the graph of number of total vaccinations
        plot4 = figure(
            title="Number of total vaccinations from " + date_filter + " to " + end_date_filter + " in " + country_filter,
            x_range=month_list,
            plot_width=1000,
            plot_height=400)
        plot4.vbar(graph_date_list, width=0.5, bottom=0, top=vac_list, color="firebrick")
        plot4.left[0].formatter.use_scientific = False
        script4, div4 = components(plot4)

        # Plot the graph of total cases
        plot2 = figure(
            title="Number of Total cases from " + date_filter + " to " + end_date_filter + " in " + country_filter,
            x_range=month_list,
            plot_width=1000,
            plot_height=400)

        plot2.vbar(graph_date_list, width=0.5, bottom=0, top=cases_list, color="firebrick")
        plot2.left[0].formatter.use_scientific = False
        script2, div2 = components(plot2)

        # Plot the scatter plot for number of deaths vs the number of people vaccinated
        x_scatter_vac_pop = vac_pop_list
        y_scatter_death = deaths_list

        scatter_plot_1 = figure(plot_width=700, plot_height=700, x_axis_label='Number of People Vaccinated',
                                y_axis_label='Number of COVID 19 Deaths in ' + country_filter)
        scatter_plot_1.circle(x_scatter_vac_pop, y_scatter_death, size=10, line_color="navy", fill_color="orange",
                              fill_alpha=0.5)
        scatter_plot_1.left[0].formatter.use_scientific = False
        scatter_plot_1.below[0].formatter.use_scientific = False

        # Best-fit Line
        d = pandas.DataFrame(x_scatter_vac_pop)
        d1 = pandas.DataFrame(y_scatter_death)
        x = np.array(d[0])
        y = np.array(d1[0])

        par = np.polyfit(x, y, 1, full=True)
        slope = par[0][0]
        intercept = par[0][1]
        y_predicted_pop = [slope * i + intercept for i in x]
        scatter_plot_1.line(x, y_predicted_pop, color='red')
        script_vac_pop_death, div_vac_pop_death = components(scatter_plot_1)

        # Plot the scatter plot for number of deaths vs the number of total vaccinations
        x_scatter_vac = vac_list
        y_scatter_death = deaths_list

        scatter_plot_2 = figure(plot_width=700, plot_height=700, x_axis_label='Number of Total Vaccinations',
                                y_axis_label='Number of COVID 19 Deaths in ' + country_filter)
        scatter_plot_2.circle(x_scatter_vac_pop, y_scatter_death, size=10, line_color="navy", fill_color="orange",
                              fill_alpha=0.5)
        scatter_plot_2.left[0].formatter.use_scientific = False
        scatter_plot_2.below[0].formatter.use_scientific = False

        # Best-fit Line
        d = pandas.DataFrame(x_scatter_vac)
        d1 = pandas.DataFrame(y_scatter_death)
        x = np.array(d[0])
        y = np.array(d1[0])

        par = np.polyfit(x, y, 1, full=True)
        slope = par[0][0]
        intercept = par[0][1]
        y_predicted_pop = [slope * i + intercept for i in x]
        scatter_plot_2.line(x, y_predicted_pop, color='red')
        script_vac_death, div_vac_death = components(scatter_plot_2)

        # Plot the scatter plot for number of cases vs the number of people vaccinated
        x_scatter_vac_pop = vac_pop_list
        y_scatter_cases = cases_list

        scatter_plot_3 = figure(plot_width=700, plot_height=700, x_axis_label='Number of People Vaccinated',
                                y_axis_label='Number of COVID 19 Cases in ' + country_filter)
        scatter_plot_3.circle(x_scatter_vac_pop, y_scatter_death, size=10, line_color="navy", fill_color="orange",
                              fill_alpha=0.5)
        scatter_plot_3.left[0].formatter.use_scientific = False
        scatter_plot_3.below[0].formatter.use_scientific = False

        # Best-fit Line
        d = pandas.DataFrame(x_scatter_vac_pop)
        d1 = pandas.DataFrame(y_scatter_cases)
        x = np.array(d[0])
        y = np.array(d1[0])

        par = np.polyfit(x, y, 1, full=True)
        slope = par[0][0]
        intercept = par[0][1]
        y_predicted_pop = [slope * i + intercept for i in x]
        scatter_plot_3.line(x, y_predicted_pop, color='red')
        script_vac_pop_case, div_vac_pop_case = components(scatter_plot_3)

        # Plot the scatter plot for number of cases vs the number of total vaccinations
        x_scatter_vac = vac_list
        y_scatter_cases = cases_list

        scatter_plot_4 = figure(plot_width=700, plot_height=700, x_axis_label='Number of Total Vaccinations',
                                y_axis_label='Number of COVID 19 Cases in ' + country_filter)
        scatter_plot_4.circle(x_scatter_vac_pop, y_scatter_death, size=10, line_color="navy", fill_color="orange",
                              fill_alpha=0.5)
        scatter_plot_4.left[0].formatter.use_scientific = False
        scatter_plot_4.below[0].formatter.use_scientific = False

        # Best-fit Line
        d = pandas.DataFrame(x_scatter_vac)
        d1 = pandas.DataFrame(y_scatter_cases)
        x = np.array(d[0])
        y = np.array(d1[0])

        par = np.polyfit(x, y, 1, full=True)
        slope = par[0][0]
        intercept = par[0][1]
        y_predicted_pop = [slope * i + intercept for i in x]
        scatter_plot_4.line(x, y_predicted_pop, color='red')
        script_vac_case, div_vac_case = components(scatter_plot_4)

        context = {'Covid19': query_result, 'script4': script4, 'div4': div4, 'script2': script2, 'div2': div2,
                   'script3': script3, 'div3': div3,
                   'script_vac_pop_death': script_vac_pop_death, 'div_vac_pop_death': div_vac_pop_death
            , 'script_vac_death': script_vac_death, 'div_vac_death': div_vac_death,
                   'script_vac_pop_case': script_vac_case, 'div_vac_pop_case': div_vac_case,
                   'script_vac_case': script_vac_case, 'div_vac_case': div_vac_case}

        return render(request, 'covid19/covid19_public_health_vac_stat.html', context)

    return render(request, 'covid19/covid19_public_health_vac_stat.html')


def covid19_socioeconomic_factor(request):
    return render(request, 'covid19/covid19_socioeconomic_factor.html')


def covid19_stringency(request):
    if request.GET.get("Location") and request.GET.get("start_date") and request.GET.get("end_date"):
        country_filter = request.GET.get("Location")
        date_filter = request.GET.get("start_date")
        end_date_filter = request.GET.get("end_date")
        processed_date_list = date_filter.split("-")
        end_processed_date_list = end_date_filter.split("-")
        date_ready = datetime.datetime(int(processed_date_list[0]), int(processed_date_list[1]),
                                       int(processed_date_list[2]))
        end_date_ready = datetime.datetime(int(end_processed_date_list[0]), int(end_processed_date_list[1]),
                                           int(end_processed_date_list[2]))
        query_result = Covid19.objects.filter(Q(location=country_filter) & Q(date__gte=date_filter))

        cases_list = []
        deaths_list = []
        stringency_list = []

        # Create a list to hold the dates that have been included
        date_list = []
        dayIncrement = datetime.timedelta(days=1)
        counter = 0

        # Find out the actual starting date in the database for that country
        while Covid19.objects.filter(Q(location=country_filter)
                                     & Q(date=date_ready)).exists() is False:
            date_ready += dayIncrement

        index = date_ready

        # Prepare date list
        while index <= end_date_ready:
            date_list.append(date_ready.isoformat())
            date_ready += dayIncrement
            index += dayIncrement
            counter += 1

        # Prepare tests and cases stats
        i = 0
        j = 0
        k = 0
        for cases in query_result.values_list('total_cases'):
            if i <= counter:
                cases_list.append(cases)
                i += 1

        for death in query_result.values_list('total_deaths'):
            if j <= counter:
                deaths_list.append(death)
                j += 1

        for stringency_index in query_result.values_list('stringency_index'):
            if k <= counter:
                stringency_list.append(stringency_index)
                k += 1

        # Reformat the dates for plotting
        graph_date_list = []
        for x in range(len(date_list)):
            reformatted_date_list = date_list[x].split("-")
            if reformatted_date_list[0] == "2020":
                if reformatted_date_list[1] == "01":
                    graph_date_list.append("2020/01")
                elif reformatted_date_list[1] == "02":
                    graph_date_list.append("2020/02")
                elif reformatted_date_list[1] == "03":
                    graph_date_list.append("2020/03")
                elif reformatted_date_list[1] == "04":
                    graph_date_list.append("2020/04")
                elif reformatted_date_list[1] == "05":
                    graph_date_list.append("2020/05")
                elif reformatted_date_list[1] == "06":
                    graph_date_list.append("2020/06")
                elif reformatted_date_list[1] == "07":
                    graph_date_list.append("2020/07")
                elif reformatted_date_list[1] == "08":
                    graph_date_list.append("2020/08")
                elif reformatted_date_list[1] == "09":
                    graph_date_list.append("2020/09")
                elif reformatted_date_list[1] == "10":
                    graph_date_list.append("2020/10")
                elif reformatted_date_list[1] == "11":
                    graph_date_list.append("2020/11")
                elif reformatted_date_list[1] == "12":
                    graph_date_list.append("2020/12")

            else:
                if reformatted_date_list[1] == "01":
                    graph_date_list.append("2021/01")
                elif reformatted_date_list[1] == "02":
                    graph_date_list.append("2021/02")
                elif reformatted_date_list[1] == "03":
                    graph_date_list.append("2021/03")
                elif reformatted_date_list[1] == "04":
                    graph_date_list.append("2021/04")
                elif reformatted_date_list[1] == "05":
                    graph_date_list.append("2021/05")
                elif reformatted_date_list[1] == "06":
                    graph_date_list.append("2021/06")
                elif reformatted_date_list[1] == "07":
                    graph_date_list.append("2021/07")
                elif reformatted_date_list[1] == "08":
                    graph_date_list.append("2021/08")
                elif reformatted_date_list[1] == "09":
                    graph_date_list.append("2021/09")
                elif reformatted_date_list[1] == "10":
                    graph_date_list.append("2021/10")
                elif reformatted_date_list[1] == "11":
                    graph_date_list.append("2021/11")
                elif reformatted_date_list[1] == "12":
                    graph_date_list.append("2021/12")

        month_list = ["2020/01", "2020/02", "2020/03", "2020/04", "2020/05", "2020/06", "2020/07",
                      "2020/08", "2020/09", "2020/10", "2020/11", "2020/12",
                      "2021/01", "2021/02", "2021/03", "2021/04"]

        # Plot the line graph for stringency index
        plot_stringency = figure(
            title="Stringency Index from " + date_filter + " to " + end_date_filter + " in " + country_filter,
            x_range=month_list, y_range=((0,10)),
            plot_width=1000,
            plot_height=400)
        plot_stringency.left[0].formatter.use_scientific = False
        plot_stringency.line(month_list, stringency_list, line_width=6)
        script_str, div_str = components(plot_stringency)

        # Plot scatter plot for cases vs stringency index
        x_scatter_str = stringency_list
        y_scatter_cases = cases_list

        scatter_plot_case_str = figure(plot_width=700, plot_height=700, x_axis_label='Stringency Index',
                                y_axis_label='Number of COVID 19 Cases in ' + country_filter)
        scatter_plot_case_str.circle(x_scatter_str, y_scatter_cases, size=10, line_color="navy", fill_color="orange",
                              fill_alpha=0.5)
        scatter_plot_case_str.left[0].formatter.use_scientific = False
        scatter_plot_case_str.below[0].formatter.use_scientific = False

         #Best-fit Line
        # d = pandas.DataFrame(x_scatter_str)
        # d1 = pandas.DataFrame(y_scatter_cases)
        # x = np.array(d[0])
        # y = np.array(d1[0])
        #
        # par = np.polyfit(x, y, 1, full=True)
        # slope = par[0][0]
        # intercept = par[0][1]
        # y_predicted_pop = [slope * i + intercept for i in x]
        # scatter_plot_case_str.line(x, y_predicted_pop, color='red')
        script_plot_case_str, div_plot_case_str = components(scatter_plot_case_str)

        # Plot scatter plot for deaths vs stringency index
        x_scatter_str = stringency_list
        y_scatter_deaths = deaths_list

        scatter_plot_death_str = figure(plot_width=700, plot_height=700, x_axis_label='Stringency Index',
                                       y_axis_label='Number of COVID 19 Deaths in ' + country_filter)
        scatter_plot_death_str.circle(x_scatter_str, y_scatter_deaths, size=10, line_color="navy", fill_color="orange",
                                     fill_alpha=0.5)
        scatter_plot_death_str.left[0].formatter.use_scientific = False
        scatter_plot_death_str.below[0].formatter.use_scientific = False

        # Best-fit Line
        # d = pandas.DataFrame(x_scatter_str)
        # d1 = pandas.DataFrame(y_scatter_cases)
        # x = np.array(d[0])
        # y = np.array(d1[0])
        #
        # par = np.polyfit(x, y, 1, full=True)
        # slope = par[0][0]
        # intercept = par[0][1]
        # y_predicted_pop = [slope * i + intercept for i in x]
        # scatter_plot_death_str.line(x, y_predicted_pop, color='red')
        script_plot_death_str, div_plot_death_str = components(scatter_plot_death_str)

        context = {'Covid19': query_result, 'script_str': script_str, 'div_str': div_str,
        'script_plot_case_str': script_plot_case_str, 'div_plot_case_str':div_plot_case_str,
        'script_plot_death_str': script_plot_death_str, 'div_plot_death_str':div_plot_death_str}
        return render(request, 'covid19/covid19_stringency.html', context)
    return render(request, 'covid19/covid19_stringency.html')

def covid19_aged_pop_stat(request):
    if request.GET.get("Location") and request.GET.get("start_date"):
        country_filter = request.GET.get("Location")
        date_filter = request.GET.get("start_date")
        query_result = Covid19.objects.filter(Q(location=country_filter) & Q(date__gte=date_filter))

        cases_list = []
        deaths_list = []
        aged_65_older_list = []
        aged_70_older_list = []

        for result in query_result:
            cases_list.append(result.total_cases)
            deaths_list.append(result.total_deaths)
            aged_65_older_list.append(result.aged_65_older)
            aged_70_older_list.append(result.aged_70_older)


        # Plot scatter plot for cases vs proportion of population aged 65 or above
        x_scatter_pop_65 = aged_65_older_list
        y_scatter_cases = cases_list

        scatter_plot_case_65 = figure(plot_width=700, plot_height=700, x_axis_label='Proportion of population aged 65 or above',
                                        y_axis_label='Number of COVID 19 Cases in ' + country_filter)
        scatter_plot_case_65.circle(x_scatter_pop_65, y_scatter_cases, size=10, line_color="navy", fill_color="orange",
                                      fill_alpha=0.5)
        scatter_plot_case_65.left[0].formatter.use_scientific = False
        scatter_plot_case_65.below[0].formatter.use_scientific = False
        script_65_case, div_65_case = components(scatter_plot_case_65)

        # Plot scatter plot for deaths vs proportion of population aged 65 or above
        x_scatter_pop_65 = aged_65_older_list
        y_scatter_deaths = deaths_list

        scatter_plot_death_65 = figure(plot_width=700, plot_height=700,
                                      x_axis_label='Proportion of population aged 65 or above',
                                      y_axis_label='Number of COVID 19 Deaths in ' + country_filter)
        scatter_plot_death_65.circle(x_scatter_pop_65, y_scatter_deaths, size=10, line_color="navy", fill_color="orange",
                                    fill_alpha=0.5)
        scatter_plot_death_65.left[0].formatter.use_scientific = False
        scatter_plot_death_65.below[0].formatter.use_scientific = False
        script_65_death, div_65_death = components(scatter_plot_death_65)

        # Plot scatter plot for cases vs proportion of population aged 70 or above
        x_scatter_pop_70 = aged_70_older_list
        y_scatter_cases = cases_list

        scatter_plot_case_70 = figure(plot_width=700, plot_height=700,
                                      x_axis_label='Proportion of population aged 70 or above',
                                      y_axis_label='Number of COVID 19 Cases in ' + country_filter)
        scatter_plot_case_70.circle(x_scatter_pop_70, y_scatter_cases, size=10, line_color="navy", fill_color="orange",
                                    fill_alpha=0.5)
        scatter_plot_case_70.left[0].formatter.use_scientific = False
        scatter_plot_case_70.below[0].formatter.use_scientific = False
        script_70_case, div_70_case = components(scatter_plot_case_70)

        # Plot scatter plot for deaths vs proportion of population aged 65 or above
        x_scatter_pop_70 = aged_70_older_list
        y_scatter_deaths = deaths_list

        scatter_plot_death_70 = figure(plot_width=700, plot_height=700,
                                       x_axis_label='Proportion of population aged 65 or above',
                                       y_axis_label='Number of COVID 19 Deaths in ' + country_filter)
        scatter_plot_death_70.circle(x_scatter_pop_70, y_scatter_deaths, size=10, line_color="navy",
                                     fill_color="orange",
                                     fill_alpha=0.5)
        scatter_plot_death_70.left[0].formatter.use_scientific = False
        scatter_plot_death_70.below[0].formatter.use_scientific = False
        script_70_death, div_70_death = components(scatter_plot_death_70)

        context = {'Covid19': query_result,'script_65_case': script_65_case
            , 'div_65_case': div_65_case, 'script_65_death': script_65_death, 'div_65_death':div_65_death,
                   'script_70_case':script_70_case, 'div_70_case': div_70_case,
                   'script_70_death':script_70_death, 'div_70_death': div_70_death}

        return render(request, 'covid19/covid19_aged_pop_stat.html', context)
    return render(request, 'covid19/covid19_aged_pop_stat.html')

def covid19_public_health_facility(request):
    return render(request, 'covid19/covid19_public_health_facility.html')


def covid19_public_health_statistics(request):
    return render(request, 'covid19/covid19_public_health_statistics.html')
