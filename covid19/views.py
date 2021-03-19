import decimal
import time
from math import pi

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

        query_result = query_result.exclude( location="World").exclude(location="North America").exclude(location="European Union").exclude(location="Asia").exclude(location="South America").exclude(location="Oceania").exclude(location="Africa").exclude(location="Georgia").exclude(location="Chad").exclude(location="Jordan")

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
            #folium.Marker(location=[co[5], co[6]], popup=popup).add_to(map_demo)
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
        result = result.exclude( location="World").exclude(location="North America").exclude(location="European Union").exclude(location="Asia").exclude(location="South America").exclude(location="Oceania").exclude(location="Africa").exclude(location="Georgia").exclude(location="Chad").exclude(location="Jordan")
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
        #combined_df['log_total_cases'] = np.log10(combined_df['total_deaths'])
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


def covid19_public_health_facility(request):
    return render(request, 'covid19/covid19_public_health_facility.html')


def covid19_public_health_statistics(request):
    return render(request, 'covid19/covid19_public_health_statistics.html')


def covid19_socioeconomic_factor(request):
    return render(request, 'covid19/covid19_socioeconomic_factor.html')
