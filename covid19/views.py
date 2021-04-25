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
from sklearn.metrics import r2_score



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
        plot5.vbar(graph_date_list, width=0.5, bottom=0, top=icu_list, color="firebrick")
        script5, div5 = components(plot5)

        # Plot number of COVID 19 patients admitted into hospitals
        plot6 = figure(
            title="Number of COVID 19 Patients Admitted into hospitals from " + start_date + " to " + end_date,
            x_range=month_list,
            plot_width=800, plot_height=400)
        plot6.left[0].formatter.use_scientific = False
        # lot3.line(graph_date_list, deaths_list, line_width=2)
        plot6.vbar(graph_date_list, width=0.5, bottom=0, top=hosp_list, color="firebrick")
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
                   + """<br>Deaths: """ + str(co[1]) \
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
                   + """<br>Deaths: """ + str(co[1]) \
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
    obtained_country = request.GET.get("Location")
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

    slider_test_list =[]
    slider_vac_list =[]
    slider_vac_pop_list=[]
    slider_str_list=[]

    if obtained_feature == "total_cases":
        if obtained_country == "World":
            result = Covid19.objects.filter(date__gte=date)
        else:
            result = Covid19.objects.filter(Q(date__gte=date) & Q(location=obtained_country))
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
        #df_slider['total_cases'] = df_slider['total_cases'].diff()


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
        if obtained_country == "World":
            result = Covid19.objects.filter(date__gte=date)
        else:
            result = Covid19.objects.filter(Q(date__gte=date) & Q(location=obtained_country))
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

        combined_df = combined_df[['location', 'total_deaths', 'date', 'geometry']]

        # Format date
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
        if obtained_country == "World":
            result = Covid19.objects.filter(date__gte=date)
        else:
            result = Covid19.objects.filter(Q(date__gte=date) & Q(location=obtained_country))
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
        if obtained_country == "World":
            result = Covid19.objects.filter(date__gte=date)
        else:
            result = Covid19.objects.filter(Q(date__gte=date) & Q(location=obtained_country))
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
        if obtained_country == "World":
            result = Covid19.objects.filter(date__gte=date)
        else:
            result = Covid19.objects.filter(Q(date__gte=date) & Q(location=obtained_country))
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

    elif obtained_feature == "total_tests":
        if obtained_country == "World":
            result = Covid19.objects.filter(date__gte=date)
        else:
            result = Covid19.objects.filter(Q(date__gte=date) & Q(location=obtained_country))
        result = result.exclude(location="World").exclude(location="North America").exclude(
            location="European Union").exclude(location="Asia").exclude(location="South America").exclude(
            location="Oceania").exclude(location="Africa").exclude(location="Georgia").exclude(location="Chad").exclude(
            location="Jordan")
        for m in result:
            slider_name_list.append(m.location)
            slider_test_list.append(m.total_tests)
            slider_lat_list.append(m.Latitude)
            slider_lon_list.append(m.Longitude)
            slider_date_list.append(m.date)

        combined = zip(slider_name_list, slider_test_list, slider_date_list)
        slider_combined = list(combined)
        df_slider = pd.DataFrame(data=slider_combined, columns=['location', 'total_tests', 'date'])
        df_slider = df_slider[df_slider.total_tests != 0]

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
        combined_df['log_total_tests'] = np.log10(combined_df['total_tests'])
        combined_df = combined_df[['location', 'log_total_tests', 'date', 'geometry']]

        combined_df['date'] = pd.to_datetime(combined_df['date']).astype(int) / 10 ** 9
        combined_df['date'] = combined_df['date'].astype(int).astype(str)

        # Construct color map
        max_color = max(combined_df['log_total_tests'])
        min_color = min(combined_df['log_total_tests'])
        color_map = cm.linear.YlOrRd_09.scale(min_color, max_color)
        combined_df['color'] = combined_df['log_total_tests'].map(color_map)

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
        color_map.caption = "Number of COVID 19 Tests in log10 scale"

        m.save("covid19/covid19_cum_stat_map.html")
        m = m._repr_html_()
        context = {
            'm': m
        }
        return render(request, 'covid19/covid19_cum_stat_map.html', context)

    elif obtained_feature == "total_vaccinations":
        if obtained_country == "World":
            result = Covid19.objects.filter(date__gte=date)
        else:
            result = Covid19.objects.filter(Q(date__gte=date) & Q(location=obtained_country))
        result = result.exclude(location="World").exclude(location="North America").exclude(
            location="European Union").exclude(location="Asia").exclude(location="South America").exclude(
            location="Oceania").exclude(location="Africa").exclude(location="Georgia").exclude(location="Chad").exclude(
            location="Jordan")
        for m in result:
            slider_name_list.append(m.location)
            slider_vac_list.append(m.total_vaccinations)
            slider_lat_list.append(m.Latitude)
            slider_lon_list.append(m.Longitude)
            slider_date_list.append(m.date)

        combined = zip(slider_name_list, slider_vac_list, slider_date_list)
        slider_combined = list(combined)
        df_slider = pd.DataFrame(data=slider_combined, columns=['location', 'total_vaccinations', 'date'])
        df_slider = df_slider[df_slider.total_vaccinations != 0]

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
        combined_df['log_total_vaccinations'] = np.log10(combined_df['total_vaccinations'])
        combined_df = combined_df[['location', 'log_total_vaccinations', 'date', 'geometry']]

        combined_df['date'] = pd.to_datetime(combined_df['date']).astype(int) / 10 ** 9
        combined_df['date'] = combined_df['date'].astype(int).astype(str)

        # Construct color map
        max_color = max(combined_df['log_total_vaccinations'])
        min_color = min(combined_df['log_total_vaccinations'])
        color_map = cm.linear.YlOrRd_09.scale(min_color, max_color)
        combined_df['color'] = combined_df['log_total_vaccinations'].map(color_map)

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
        color_map.caption = "Number of COVID 19 Vaccinations in log10 scale"

        m.save("covid19/covid19_cum_stat_map.html")
        m = m._repr_html_()
        context = {
            'm': m
        }
        return render(request, 'covid19/covid19_cum_stat_map.html', context)

    elif obtained_feature == "people_vaccinated":
        if obtained_country == "World":
            result = Covid19.objects.filter(date__gte=date)
        else:
            result = Covid19.objects.filter(Q(date__gte=date) & Q(location=obtained_country))
        result = result.exclude(location="World").exclude(location="North America").exclude(
            location="European Union").exclude(location="Asia").exclude(location="South America").exclude(
            location="Oceania").exclude(location="Africa").exclude(location="Georgia").exclude(location="Chad").exclude(
            location="Jordan")
        for m in result:
            slider_name_list.append(m.location)
            slider_vac_pop_list.append(m.people_vaccinated)
            slider_lat_list.append(m.Latitude)
            slider_lon_list.append(m.Longitude)
            slider_date_list.append(m.date)

        combined = zip(slider_name_list, slider_vac_pop_list, slider_date_list)
        slider_combined = list(combined)
        df_slider = pd.DataFrame(data=slider_combined, columns=['location', 'people_vaccinated', 'date'])
        df_slider = df_slider[df_slider.people_vaccinated != 0]

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
        combined_df['log_people_vaccinated'] = np.log10(combined_df['people_vaccinated'])
        combined_df = combined_df[['location', 'log_people_vaccinated', 'date', 'geometry']]

        combined_df['date'] = pd.to_datetime(combined_df['date']).astype(int) / 10 ** 9
        combined_df['date'] = combined_df['date'].astype(int).astype(str)

        # Construct color map
        max_color = max(combined_df['log_people_vaccinated'])
        min_color = min(combined_df['log_people_vaccinated'])
        color_map = cm.linear.YlOrRd_09.scale(min_color, max_color)
        combined_df['color'] = combined_df['log_people_vaccinated'].map(color_map)

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
        color_map.caption = "Number of people vaccinated in log10 scale"

        m.save("covid19/covid19_cum_stat_map.html")
        m = m._repr_html_()
        context = {
            'm': m
        }
        return render(request, 'covid19/covid19_cum_stat_map.html', context)

    elif obtained_feature == "stringency_index":
        if obtained_country == "World":
            result = Covid19.objects.filter(date__gte=date)
        else:
            result = Covid19.objects.filter(Q(date__gte=date) & Q(location=obtained_country))
        result = result.exclude(location="World").exclude(location="North America").exclude(
            location="European Union").exclude(location="Asia").exclude(location="South America").exclude(
            location="Oceania").exclude(location="Africa").exclude(location="Georgia").exclude(location="Chad").exclude(
            location="Jordan")
        for m in result:
            slider_name_list.append(m.location)
            slider_str_list.append(m.stringency_index)
            slider_lat_list.append(m.Latitude)
            slider_lon_list.append(m.Longitude)
            slider_date_list.append(m.date)

        combined = zip(slider_name_list, slider_str_list, slider_date_list)
        slider_combined = list(combined)
        df_slider = pd.DataFrame(data=slider_combined, columns=['location', 'stringency_index', 'date'])
        df_slider = df_slider[df_slider.stringency_index != 0]

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
        combined_df['stringency_index'] = pd.to_numeric(combined_df['stringency_index'])
        combined_df = combined_df[['location', 'stringency_index', 'date', 'geometry']]

        combined_df['date'] = pd.to_datetime(combined_df['date']).astype(int) / 10 ** 9
        combined_df['date'] = combined_df['date'].astype(int).astype(str)

        # Construct color map
        max_color = max(combined_df['stringency_index'])
        min_color = min(combined_df['stringency_index'])
        color_map = cm.linear.YlOrRd_09.scale(min_color, max_color)
        combined_df['color'] = combined_df['stringency_index'].map(color_map)

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
        color_map.caption = "Stringency Index in integer scale"

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
        query_result = Covid19.objects.filter(Q(location=country_filter) & Q(date__gte=date_filter)
                                              & ~Q(total_cases=0) & ~Q(total_tests=0))

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
        plot2 = figure(title="Number of Total cases from " + date_filter + " to " + end_date_filter + " in " + country_filter,
                       x_range=month_list,
                       plot_width=1000,
                       plot_height=400)

        plot2.vbar(graph_date_list, width=0.5, bottom=0, top=cases_list, color="firebrick")
        plot2.left[0].formatter.use_scientific = False
        script2, div2 = components(plot2)

        # Plot the graph of total tests
        plot3 = figure(title="Number of total tests from " + date_filter + " to " + end_date_filter + " in " + country_filter,
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

        # R^2
        r2_value = r2_score(y,y_predicted_pop)

        context = {'Covid19': query_result, 'script2': script2, 'div2': div2, 'script3': script3, 'div3': div3,
                   'script_test_case': script_test_case, 'div_test_case': div_test_case,
                   'r2_value':r2_value}

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
        query_result = Covid19.objects.filter(Q(location=country_filter) & Q(date__gte=date_filter)
                                              & ~Q(total_vaccinations=0) & ~Q(people_vaccinated=0)
                                              & ~Q(total_deaths=0) & ~Q(total_cases=0))

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
        r2_1 =r2_score(y,y_predicted_pop)

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
        r2_2 = r2_score(y,y_predicted_pop)

        # Plot the scatter plot for number of cases vs the number of people vaccinated
        x_scatter_vac_pop = vac_pop_list
        y_scatter_cases = cases_list

        scatter_plot_3 = figure(plot_width=700, plot_height=700, x_axis_label='Number of People Vaccinated',
                                y_axis_label='Number of COVID 19 Cases in ' + country_filter)
        scatter_plot_3.circle(x_scatter_vac_pop, y_scatter_cases, size=10, line_color="navy", fill_color="orange",
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
        r2_3 = r2_score(y,y_predicted_pop)

        # Plot the scatter plot for number of cases vs the number of total vaccinations
        x_scatter_vac = vac_list
        y_scatter_cases = cases_list

        scatter_plot_4 = figure(plot_width=700, plot_height=700, x_axis_label='Number of Total Vaccinations',
                                y_axis_label='Number of COVID 19 Cases in ' + country_filter)
        scatter_plot_4.circle(x_scatter_vac_pop, y_scatter_cases, size=10, line_color="navy", fill_color="orange",
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
        r2_4 = r2_score(y,y_predicted_pop)
        script_vac_case, div_vac_case = components(scatter_plot_4)

        context = {'Covid19': query_result, 'script4': script4, 'div4': div4, 'script2': script2, 'div2': div2,
                   'script3': script3, 'div3': div3,
                   'script_vac_pop_death': script_vac_pop_death, 'div_vac_pop_death': div_vac_pop_death
            , 'script_vac_death': script_vac_death, 'div_vac_death': div_vac_death,
                   'script_vac_pop_case': script_vac_pop_case, 'div_vac_pop_case': div_vac_pop_case,
                   'script_vac_case': script_vac_case, 'div_vac_case': div_vac_case,
                   'r2_1':r2_1, 'r2_2':r2_2, 'r2_3':r2_3, 'r2_4':r2_4}

        return render(request, 'covid19/covid19_public_health_vac_stat.html', context)

    return render(request, 'covid19/covid19_public_health_vac_stat.html')


def covid19_socioeconomic_factor(request):
    return render(request, 'covid19/covid19_socioeconomic_factor.html')


def covid19_stringency(request):
    if request.GET.get("Location") and request.GET.get("start_date") and request.GET.get("end_date") and request.GET.get("str_lower"):
        country_filter = request.GET.get("Location")
        date_filter = request.GET.get("start_date")
        end_date_filter = request.GET.get("end_date")
        str_lower = request.GET.get("str_lower")
        processed_date_list = date_filter.split("-")
        end_processed_date_list = end_date_filter.split("-")
        date_ready = datetime.datetime(int(processed_date_list[0]), int(processed_date_list[1]),
                                       int(processed_date_list[2]))
        end_date_ready = datetime.datetime(int(end_processed_date_list[0]), int(end_processed_date_list[1]),
                                           int(end_processed_date_list[2]))
        query_result = Covid19.objects.filter(Q(location=country_filter) & Q(date__gte=date_filter) & Q(stringency_index__gte=str_lower))

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

        #Prepare date list
        while index <= end_date_ready:
            date_list.append(date_ready.isoformat())
            date_ready += dayIncrement
            index += dayIncrement
            counter += 1

        # Prepare tests and cases stats
        i = 0
        j = 0
        k = 0
        for cases in query_result.values_list('total_cases',flat=True):
            if i <= counter:
                cases_list.append(cases)
                i += 1

        for death in query_result.values_list('total_deaths',flat=True):
            if j <= counter:
                deaths_list.append(death)
                j += 1

        for stringency_index in query_result.values_list('stringency_index',flat=True):
            if k <= counter:
                stringency_list.append(stringency_index)
                k += 1
        print(stringency_list)
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
            title="Stringency Index " + date_filter + " to " + " in " + country_filter,
            x_range=month_list, y_range=((0, 10)),
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
        #scatter_plot_case_str.circle(x_scatter_str, y_scatter_cases, size=10, line_color="navy", fill_color="orange",
                                    # fill_alpha=0.5)
        scatter_plot_case_str.vbar(x_scatter_str, width=0.8,bottom=0,top=y_scatter_cases,color="orange")
        scatter_plot_case_str.left[0].formatter.use_scientific = False
        scatter_plot_case_str.below[0].formatter.use_scientific = False



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
        # scatter_plot_case_str.line(x, y_predicted_pop, color='red')
        script_plot_case_str, div_plot_case_str = components(scatter_plot_case_str)

        # Plot scatter plot for deaths vs stringency index
        x_scatter_str = stringency_list
        y_scatter_deaths = deaths_list

        scatter_plot_death_str = figure(plot_width=700, plot_height=700, x_axis_label='Stringency Index',
                                        y_axis_label='Number of COVID 19 Deaths in ' + country_filter)
        #scatter_plot_death_str.circle(x_scatter_str, y_scatter_deaths, size=10, line_color="navy", fill_color="orange",
                                      #fill_alpha=0.5)
        scatter_plot_death_str.vbar(x_scatter_str,width=0.8,bottom=0,top=y_scatter_deaths,color="blue")
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
                   'script_plot_case_str': script_plot_case_str, 'div_plot_case_str': div_plot_case_str,
                   'script_plot_death_str': script_plot_death_str, 'div_plot_death_str': div_plot_death_str}
        return render(request, 'covid19/covid19_stringency.html', context)
    return render(request, 'covid19/covid19_stringency.html')


def covid19_aged_pop_stat(request):
    if request.GET.get("Location") and request.GET.get("start_date"):
        country_filter = request.GET.get("Location")
        date_filter = request.GET.get("start_date")
        query_result = Covid19.objects.filter(Q(continent=country_filter) & Q(date__gte=date_filter))

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

        scatter_plot_case_65 = figure(plot_width=700, plot_height=700,
                                      x_axis_label='Proportion of population aged 65 or above',
                                      y_axis_label='Number of COVID 19 Cases in ' + country_filter)
        scatter_plot_case_65.circle(x_scatter_pop_65, y_scatter_cases, size=10, line_color="navy", fill_color="orange",
                                   fill_alpha=0.5)
        scatter_plot_case_65.left[0].formatter.use_scientific = False
        scatter_plot_case_65.below[0].formatter.use_scientific = False
        script_65_case, div_65_case = components(scatter_plot_case_65)

        # Bar
        scatter_plot_case_65_bar = figure(plot_width=700, plot_height=700,
                                      x_axis_label='Proportion of population aged 65 or above',
                                      y_axis_label='Number of COVID 19 Cases in ' + country_filter)
        scatter_plot_case_65_bar.vbar(x_scatter_pop_65, width=0.8, bottom=0, top=y_scatter_cases, color="firebrick")
        scatter_plot_case_65_bar.left[0].formatter.use_scientific = False
        scatter_plot_case_65_bar.below[0].formatter.use_scientific = False
        script_65_case_bar, div_65_case_bar = components(scatter_plot_case_65_bar)

        # Plot scatter plot for deaths vs proportion of population aged 65 or above
        x_scatter_pop_65 = aged_65_older_list
        y_scatter_deaths = deaths_list

        scatter_plot_death_65 = figure(plot_width=700, plot_height=700,
                                       x_axis_label='Proportion of population aged 65 or above',
                                       y_axis_label='Number of COVID 19 Deaths in ' + country_filter)
        scatter_plot_death_65.circle(x_scatter_pop_65, y_scatter_deaths, size=10, line_color="navy",
                                     fill_color="orange",
                                     fill_alpha=0.5)
        scatter_plot_death_65.left[0].formatter.use_scientific = False
        scatter_plot_death_65.below[0].formatter.use_scientific = False
        script_65_death, div_65_death = components(scatter_plot_death_65)

        #Bar
        scatter_plot_death_65_bar = figure(plot_width=700, plot_height=700,
                                       x_axis_label='Proportion of population aged 65 or above',
                                       y_axis_label='Number of COVID 19 Deaths in ' + country_filter)
        scatter_plot_death_65_bar.vbar(x_scatter_pop_65, width=0.8, bottom=0, top=y_scatter_deaths,color="orange" )
        scatter_plot_death_65_bar.left[0].formatter.use_scientific = False
        scatter_plot_death_65_bar.below[0].formatter.use_scientific = False
        script_65_death_bar, div_65_death_bar = components(scatter_plot_death_65_bar)

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

        #Bar
        scatter_plot_case_70_bar = figure(plot_width=700, plot_height=700,
                                      x_axis_label='Proportion of population aged 70 or above',
                                      y_axis_label='Number of COVID 19 Cases in ' + country_filter)
        scatter_plot_case_70_bar.vbar(x_scatter_pop_70, width=0.8, bottom=0, top=y_scatter_cases,color="blue")
        scatter_plot_case_70_bar.left[0].formatter.use_scientific = False
        scatter_plot_case_70_bar.below[0].formatter.use_scientific = False
        script_70_case_bar, div_70_case_bar = components(scatter_plot_case_70_bar)


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

        #Bar
        scatter_plot_death_70_bar = figure(plot_width=700, plot_height=700,
                                       x_axis_label='Proportion of population aged 65 or above',
                                       y_axis_label='Number of COVID 19 Deaths in ' + country_filter)
        scatter_plot_death_70_bar.vbar(x_scatter_pop_70,width=0.8, bottom=0,top=y_scatter_deaths,color="orange")
        scatter_plot_death_70_bar.left[0].formatter.use_scientific = False
        scatter_plot_death_70_bar.below[0].formatter.use_scientific = False
        script_70_death_bar, div_70_death_bar = components(scatter_plot_death_70_bar)

        query_result_table = query_result.filter(date="2021-03-15").order_by('aged_65_older','aged_70_older')
        context = {'Covid19': query_result_table, 'script_65_case': script_65_case
            , 'div_65_case': div_65_case, 'script_65_death': script_65_death, 'div_65_death': div_65_death,
                   'script_70_case': script_70_case, 'div_70_case': div_70_case,
                   'script_70_death': script_70_death, 'div_70_death': div_70_death,
                   'script_65_case_bar':script_65_case_bar, 'div_65_case_bar':div_65_case_bar,
                   'script_70_case_bar':script_70_case_bar,'div_70_case_bar':div_70_case_bar,
                   'script_65_death_bar':script_65_death_bar, 'div_65_death_bar':div_65_death_bar,
                   'script_70_death_bar':script_70_death_bar, 'div_70_death_bar':div_70_death_bar}

        return render(request, 'covid19/covid19_aged_pop_stat.html', context)
    return render(request, 'covid19/covid19_aged_pop_stat.html')


def covid19_gdp(request):
    if request.GET.get("Location") and request.GET.get("start_date"):
        country_filter = request.GET.get("Location")
        date_filter = request.GET.get("start_date")
        # if country_filter == "World":
        #     query_result = Covid19.objects.filter(Q(location="World") & Q(date__gte=date_filter))

        # else:
        query_result = Covid19.objects.filter(Q(continent=country_filter) & Q(date__gte=date_filter))

        cases_list = []
        deaths_list = []
        tests_list = []
        vac_pop_list = []
        vac_list = []
        gdp_list = []

        for result in query_result:
            cases_list.append(result.total_cases)
            deaths_list.append(result.total_deaths)
            tests_list.append(result.total_tests)
            vac_pop_list.append(result.people_vaccinated)
            vac_list.append(result.total_vaccinations)
            gdp_list.append(result.gdp_per_capita)

        # Plot scatterplot for case vs GDP
        x_scatter_gdp = gdp_list
        y_scatter_cases = cases_list

        scatter_plot_gdp_case = figure(plot_width=700, plot_height=700,
                                       x_axis_label='GDP per capita',
                                       y_axis_label='Number of COVID 19 Cases in ' + country_filter)
        scatter_plot_gdp_case.circle(x_scatter_gdp, y_scatter_cases, size=10, line_color="navy", fill_color="orange",
                                     fill_alpha=0.5)
        scatter_plot_gdp_case.left[0].formatter.use_scientific = False
        scatter_plot_gdp_case.below[0].formatter.use_scientific = False
        script_gdp_case, div_gdp_case = components(scatter_plot_gdp_case)

        scatter_plot_gdp_case_bar = figure(plot_width=700, plot_height=700,
                                       x_axis_label='GDP per capita',
                                       y_axis_label='Number of COVID 19 Cases in ' + country_filter)
        scatter_plot_gdp_case_bar.vbar(x_scatter_gdp, width=2,bottom=0,top=y_scatter_cases,color="firebrick")
        scatter_plot_gdp_case_bar.left[0].formatter.use_scientific = False
        scatter_plot_gdp_case_bar.below[0].formatter.use_scientific = False
        script_gdp_case_bar, div_gdp_case_bar = components(scatter_plot_gdp_case_bar)


        # Plot scatterplot for death vs GDP
        x_scatter_gdp = gdp_list
        y_scatter_deaths = deaths_list

        scatter_plot_gdp_death = figure(plot_width=700, plot_height=700,
                                        x_axis_label='GDP per capita',
                                        y_axis_label='Number of COVID 19 Deaths in ' + country_filter)
        scatter_plot_gdp_death.circle(x_scatter_gdp, y_scatter_deaths, size=10, line_color="navy", fill_color="orange",
                                      fill_alpha=0.5)
        scatter_plot_gdp_death.left[0].formatter.use_scientific = False
        scatter_plot_gdp_death.below[0].formatter.use_scientific = False
        script_gdp_death, div_gdp_death = components(scatter_plot_gdp_death)

        scatter_plot_gdp_death_bar = figure(plot_width=700, plot_height=700,
                                        x_axis_label='GDP per capita',
                                        y_axis_label='Number of COVID 19 Deaths in ' + country_filter)
        scatter_plot_gdp_death_bar.vbar(x_scatter_gdp, width=0.8,bottom=0,top=y_scatter_deaths,color="firebrick")
        scatter_plot_gdp_death_bar.left[0].formatter.use_scientific = False
        scatter_plot_gdp_death_bar.below[0].formatter.use_scientific = False
        script_gdp_death_bar, div_gdp_death_bar = components(scatter_plot_gdp_death_bar)

        # Plot scatterplot for test vs GDP
        x_scatter_gdp = gdp_list
        y_scatter_test = tests_list

        scatter_plot_gdp_test = figure(plot_width=700, plot_height=700,
                                       x_axis_label='GDP per capita',
                                       y_axis_label='Number of COVID 19 Tests in ' + country_filter)
        scatter_plot_gdp_test.circle(x_scatter_gdp, y_scatter_test, size=10, line_color="navy", fill_color="orange",
                                     fill_alpha=0.5)
        scatter_plot_gdp_test.left[0].formatter.use_scientific = False
        scatter_plot_gdp_test.below[0].formatter.use_scientific = False
        script_gdp_test, div_gdp_test = components(scatter_plot_gdp_test)

        scatter_plot_gdp_test_bar = figure(plot_width=700, plot_height=700,
                                       x_axis_label='GDP per capita',
                                       y_axis_label='Number of COVID 19 Tests in ' + country_filter)
        scatter_plot_gdp_test_bar.vbar(x_scatter_gdp, width=2, bottom=0,top=y_scatter_test,color="firebrick")
        scatter_plot_gdp_test_bar.left[0].formatter.use_scientific = False
        scatter_plot_gdp_test_bar.below[0].formatter.use_scientific = False
        script_gdp_test_bar, div_gdp_test_bar = components(scatter_plot_gdp_test_bar)

        # Plot scatterplot for number of people vaccinated vs GDP
        x_scatter_gdp = gdp_list
        y_scatter_vac_people = vac_pop_list

        scatter_plot_gdp_vac_pop = figure(plot_width=700, plot_height=700,
                                          x_axis_label='GDP per capita',
                                          y_axis_label='Number of vaccinated people in ' + country_filter)
        scatter_plot_gdp_vac_pop.circle(x_scatter_gdp, y_scatter_vac_people, size=10, line_color="navy",
                                        fill_color="orange",
                                        fill_alpha=0.5)
        scatter_plot_gdp_vac_pop.left[0].formatter.use_scientific = False
        scatter_plot_gdp_vac_pop.below[0].formatter.use_scientific = False
        script_gdp_vac_pop, div_gdp_vac_pop = components(scatter_plot_gdp_vac_pop)

        scatter_plot_gdp_vac_pop_bar = figure(plot_width=700, plot_height=700,
                                          x_axis_label='GDP per capita',
                                          y_axis_label='Number of vaccinated people in ' + country_filter)
        scatter_plot_gdp_vac_pop_bar.vbar(x_scatter_gdp, width=2, bottom=0,top=y_scatter_vac_people,color="firebrick")
        scatter_plot_gdp_vac_pop_bar.left[0].formatter.use_scientific = False
        scatter_plot_gdp_vac_pop_bar.below[0].formatter.use_scientific = False
        script_gdp_vac_pop_bar, div_gdp_vac_pop_bar = components(scatter_plot_gdp_vac_pop_bar)


        # Plot scatterplot for number of total vaccinations vs GDP
        x_scatter_gdp = gdp_list
        y_scatter_vac = vac_list

        scatter_plot_gdp_vac = figure(plot_width=700, plot_height=700,
                                      x_axis_label='GDP per capita',
                                      y_axis_label='Number of total vaccinations in ' + country_filter)
        scatter_plot_gdp_vac.circle(x_scatter_gdp, y_scatter_vac, size=10, line_color="navy",
                                    fill_color="orange",
                                    fill_alpha=0.5)
        scatter_plot_gdp_vac.left[0].formatter.use_scientific = False
        scatter_plot_gdp_vac.below[0].formatter.use_scientific = False
        script_gdp_vac, div_gdp_vac = components(scatter_plot_gdp_vac)

        scatter_plot_gdp_vac_bar = figure(plot_width=700, plot_height=700,
                                      x_axis_label='GDP per capita',
                                      y_axis_label='Number of total vaccinations in ' + country_filter)
        scatter_plot_gdp_vac_bar.vbar(x_scatter_gdp, width=2, bottom=0, top=y_scatter_vac,color="firebrick")
        scatter_plot_gdp_vac_bar.left[0].formatter.use_scientific = False
        scatter_plot_gdp_vac_bar.below[0].formatter.use_scientific = False
        script_gdp_vac_bar, div_gdp_vac_bar = components(scatter_plot_gdp_vac_bar)



        query_result_table = query_result.filter(date="2021-03-15").order_by('-gdp_per_capita')
        context = {'Covid19': query_result_table, 'script_gdp_case': script_gdp_case, 'div_gdp_case': div_gdp_case,
                   'script_gdp_death': script_gdp_death, 'div_gdp_death': div_gdp_death,
                   'script_gdp_test': script_gdp_test, 'div_gdp_test': div_gdp_test,
                   'script_gdp_vac_pop': script_gdp_vac_pop, 'div_gdp_vac_pop': div_gdp_vac_pop,
                   'script_gdp_vac': script_gdp_vac, 'div_gdp_vac': div_gdp_vac,
                   'script_gdp_case_bar': script_gdp_case_bar, 'div_gdp_case_bar': div_gdp_case_bar,
                   'script_gdp_death_bar': script_gdp_death_bar, 'div_gdp_death_bar': div_gdp_death_bar,
                   'script_gdp_test_bar': script_gdp_test_bar, 'div_gdp_test_bar': div_gdp_test_bar,
                   'script_gdp_vac_pop_bar': script_gdp_vac_pop_bar, 'div_gdp_vac_pop_bar': div_gdp_vac_pop_bar,
                   'script_gdp_vac_bar': script_gdp_vac_bar, 'div_gdp_vac_bar': div_gdp_vac_bar
                   }

        return render(request, 'covid19/covid19_gdp.html', context)
    return render(request, 'covid19/covid19_gdp.html')


def covid19_public_health_statistics(request):
    return render(request, 'covid19/covid19_public_health_statistics.html')


def covid19_cardiovascular_death_rate(request):
    if request.GET.get("Location") and request.GET.get("start_date"):
        country_filter = request.GET.get("Location")
        date_filter = request.GET.get("start_date")
        if country_filter == "World":
            query_result = Covid19.objects.filter(Q(location="World") & Q(date__gte=date_filter))

        else:
            query_result = Covid19.objects.filter(Q(continent=country_filter) & Q(date__gte=date_filter))

        cases_list = []
        deaths_list = []
        aged_65_list = []
        aged_70_list = []
        cardiovasc_death_rate_list = []

        for result in query_result:
            cases_list.append(result.total_cases)
            deaths_list.append(result.total_deaths)
            aged_65_list.append(result.aged_65_older)
            aged_70_list.append(result.aged_70_older)
            cardiovasc_death_rate_list.append(result.cardiovasc_death_rate)

        # Plot scatter plot for cardiovascular death rate vs percentage of 65 or above population
        x_scatter_65 = aged_65_list
        y_scatter_car = cardiovasc_death_rate_list

        scatter_plot_65_car = figure(plot_width=700, plot_height=700,
                                     x_axis_label='Percentage of 65 or above population',
                                     y_axis_label='Cardiovascular death rate in ' + country_filter)
        scatter_plot_65_car.circle(x_scatter_65, y_scatter_car, size=10, line_color="navy", fill_color="orange",
                                   fill_alpha=0.5)
        scatter_plot_65_car.left[0].formatter.use_scientific = False
        scatter_plot_65_car.below[0].formatter.use_scientific = False
        script_65_car, div_65_car = components(scatter_plot_65_car)

        # Plot scatter plot for cardiovascular death rate vs percentage of 70 or above population
        x_scatter_70 = aged_70_list
        y_scatter_car = cardiovasc_death_rate_list

        scatter_plot_70_car = figure(plot_width=700, plot_height=700,
                                     x_axis_label='Percentage of 70 or above population',
                                     y_axis_label='Cardiovascular death rate in ' + country_filter)
        scatter_plot_70_car.circle(x_scatter_70, y_scatter_car, size=10, line_color="navy", fill_color="orange",
                                   fill_alpha=0.5)
        scatter_plot_70_car.left[0].formatter.use_scientific = False
        scatter_plot_70_car.below[0].formatter.use_scientific = False
        script_70_car, div_70_car = components(scatter_plot_70_car)

        # Plot scatter plot for cases vs cardiovascular death rate
        x_scatter_car = cardiovasc_death_rate_list
        y_scatter_case = cases_list

        scatter_plot_case_car = figure(plot_width=700, plot_height=700,
                                       x_axis_label='Cardiovascular death rate',
                                       y_axis_label='Number of COVID 19 cases in ' + country_filter)
        # scatter_plot_case_car.circle(x_scatter_car, y_scatter_case, size=10, line_color="navy", fill_color="orange",
        #                              fill_alpha=0.5)
        scatter_plot_case_car.vbar(x_scatter_car, width=0.8,bottom=0, top=y_scatter_case, color="blue")
        scatter_plot_case_car.left[0].formatter.use_scientific = False
        scatter_plot_case_car.below[0].formatter.use_scientific = False
        script_case_car, div_case_car = components(scatter_plot_case_car)

        # Plot scatter plot for deaths vs cardiovascular death rate
        x_scatter_car = cardiovasc_death_rate_list
        y_scatter_death = deaths_list

        scatter_plot_death_car = figure(plot_width=700, plot_height=700,
                                        x_axis_label='Cardiovascular death rate',
                                        y_axis_label='Number of COVID 19 cases in ' + country_filter)
        # scatter_plot_death_car.circle(x_scatter_car, y_scatter_death, size=10, line_color="navy", fill_color="orange",
        #                               fill_alpha=0.5)
        scatter_plot_death_car.vbar(x_scatter_car,width=0.8,bottom=0,top=y_scatter_death,color="firebrick")
        scatter_plot_death_car.left[0].formatter.use_scientific = False
        scatter_plot_death_car.below[0].formatter.use_scientific = False
        script_death_car, div_death_car = components(scatter_plot_death_car)

        query_result_table = query_result.filter(date="2021-03-15").order_by('-cardiovasc_death_rate')
        context = {'Covid19': query_result_table, 'script_65_car': script_65_car, 'div_65_car': div_65_car,
                   'script_70_car': script_70_car, 'div_70_car': div_70_car,
                   'script_case_car': script_case_car, 'div_case_car': div_case_car,
                   'script_death_car': script_death_car, 'div_death_car': div_death_car}
        return render(request, 'covid19/covid19_cardiovascular_death_rate.html', context)
    return render(request, 'covid19/covid19_cardiovascular_death_rate.html')


def covid19_diabetes_prevalence(request):
    if request.GET.get("Location") and request.GET.get("start_date"):
        country_filter = request.GET.get("Location")
        date_filter = request.GET.get("start_date")
        if country_filter == "World":
            query_result = Covid19.objects.filter(Q(location="World") & Q(date__gte=date_filter))

        else:
            query_result = Covid19.objects.filter(Q(continent=country_filter) & Q(date__gte=date_filter))

        cases_list = []
        deaths_list = []
        aged_65_list = []
        aged_70_list = []
        dia_prev_list = []

        for result in query_result:
            cases_list.append(result.total_cases)
            deaths_list.append(result.total_deaths)
            aged_65_list.append(result.aged_65_older)
            aged_70_list.append(result.aged_70_older)
            dia_prev_list.append(result.diabetes_prevalence)

        # Plot scatter plot for diabetes prevalence rate vs percentage of 65 or above population
        x_scatter_65 = aged_65_list
        y_scatter_prev = dia_prev_list

        scatter_plot_65_prev = figure(plot_width=700, plot_height=700,
                                      x_axis_label='Percentage of 65 or above population',
                                      y_axis_label='Diabetes prevalence rate in ' + country_filter)
        scatter_plot_65_prev.circle(x_scatter_65, y_scatter_prev, size=10, line_color="navy", fill_color="orange",
                                    fill_alpha=0.5)
        scatter_plot_65_prev.left[0].formatter.use_scientific = False
        scatter_plot_65_prev.below[0].formatter.use_scientific = False
        script_65_prev, div_65_prev = components(scatter_plot_65_prev)

        # Plot scatter plot for diabetes prevalence rate  vs percentage of 70 or above population
        x_scatter_70 = aged_70_list
        y_scatter_prev = dia_prev_list

        scatter_plot_70_prev = figure(plot_width=700, plot_height=700,
                                      x_axis_label='Percentage of 70 or above population',
                                      y_axis_label='Diabetes prevalence rate in ' + country_filter)
        scatter_plot_70_prev.circle(x_scatter_70, y_scatter_prev, size=10, line_color="navy", fill_color="orange",
                                    fill_alpha=0.5)
        scatter_plot_70_prev.left[0].formatter.use_scientific = False
        scatter_plot_70_prev.below[0].formatter.use_scientific = False
        script_70_prev, div_70_prev = components(scatter_plot_70_prev)

        # Plot scatter plot for cases vs cardiovascular death rate
        x_scatter_prev = dia_prev_list
        y_scatter_case = cases_list

        scatter_plot_prev_car = figure(plot_width=700, plot_height=700,
                                       x_axis_label='Diabetes prevalence rate',
                                       y_axis_label='Number of COVID 19 cases in ' + country_filter)
        # scatter_plot_prev_car.circle(x_scatter_prev, y_scatter_case, size=10, line_color="navy", fill_color="orange",
        #                              fill_alpha=0.5)
        scatter_plot_prev_car.vbar(x_scatter_prev, width=0.3, bottom=0, top=y_scatter_case, color="blue")
        scatter_plot_prev_car.left[0].formatter.use_scientific = False
        scatter_plot_prev_car.below[0].formatter.use_scientific = False
        script_prev_car, div_prev_car = components(scatter_plot_prev_car)

        # Plot scatter plot for deaths vs cardiovascular death rate
        x_scatter_prev = dia_prev_list
        y_scatter_death = deaths_list

        scatter_plot_death_prev = figure(plot_width=700, plot_height=700,
                                         x_axis_label='Diabetes prevalence rate',
                                         y_axis_label='Number of COVID 19 deaths in ' + country_filter)
        # scatter_plot_death_prev.circle(x_scatter_prev, y_scatter_death, size=10, line_color="navy", fill_color="orange",
        #                                fill_alpha=0.5)
        scatter_plot_death_prev.vbar(x_scatter_prev, width=0.3, bottom=0, top=y_scatter_death, color="red")
        scatter_plot_death_prev.left[0].formatter.use_scientific = False
        scatter_plot_death_prev.below[0].formatter.use_scientific = False
        script_death_prev, div_death_prev = components(scatter_plot_death_prev)

        query_result_table = query_result.filter(date="2021-03-15").order_by('-diabetes_prevalence')
        context = {'Covid19': query_result_table, 'script_65_prev': script_65_prev, 'div_65_prev': div_65_prev,
                   'script_70_prev': script_70_prev, 'div_70_prev': div_70_prev,
                   'script_prev_car': script_prev_car, 'div_prev_car': div_prev_car,
                   'script_death_prev': script_death_prev, 'div_death_prev': div_death_prev}
        return render(request, 'covid19/covid19_diabetes_prevalence.html', context)
    return render(request, 'covid19/covid19_diabetes_prevalence.html')


def covid19_public_health_facility(request):
    return render(request, 'covid19/covid19_public_health_facility.html')


def covid19_handwashing(request):
    if request.GET.get("Location") and request.GET.get("start_date"):
        country_filter = request.GET.get("Location")
        date_filter = request.GET.get("start_date")
        if country_filter == "World":
            query_result = Covid19.objects.filter(Q(location="World") & Q(date__gte=date_filter))

        else:
            query_result = Covid19.objects.filter(Q(continent=country_filter) & Q(date__gte=date_filter))

        cases_list = []
        deaths_list = []
        handwashing_list = []

        for result in query_result:
            cases_list.append(result.total_cases)
            deaths_list.append(result.total_deaths)
            handwashing_list.append(result.handwashing_facilities)

        # Plot scatter plot for covid 19 cases vs share of population with basic handwashing facilities
        x_scatter_wash = handwashing_list
        y_scatter_cases = cases_list

        scatter_plot_wash_case = figure(plot_width=700, plot_height=700,
                                        x_axis_label='Share of population with basic handwashing facilities',
                                        y_axis_label='Number of COVID 19 cases in ' + country_filter)
        # scatter_plot_wash_case.circle(x_scatter_wash, y_scatter_cases, size=10, line_color="navy", fill_color="orange",
        #                               fill_alpha=0.5)
        scatter_plot_wash_case.vbar(x_scatter_wash, width=0.8, bottom=0, top=y_scatter_cases, color="blue")
        scatter_plot_wash_case.left[0].formatter.use_scientific = False
        scatter_plot_wash_case.below[0].formatter.use_scientific = False
        script_wash_case, div_wash_case = components(scatter_plot_wash_case)

        # Plot scatter plot for covid 19 deaths vs share of population with basic handwashing facilities
        x_scatter_wash = handwashing_list
        y_scatter_deaths = deaths_list

        scatter_plot_wash_death = figure(plot_width=700, plot_height=700,
                                         x_axis_label='Share of population with basic handwashing facilities',
                                         y_axis_label='Number of COVID 19 deaths in ' + country_filter)
        # scatter_plot_wash_death.circle(x_scatter_wash, y_scatter_deaths, size=10, line_color="navy",
        #                                fill_color="orange",
        #                                fill_alpha=0.5)
        scatter_plot_wash_death.vbar(x_scatter_wash, width=0.8, bottom=0,top=y_scatter_deaths, color="red")
        scatter_plot_wash_death.left[0].formatter.use_scientific = False
        scatter_plot_wash_death.below[0].formatter.use_scientific = False
        script_wash_death, div_wash_death = components(scatter_plot_wash_death)

        query_result_table = query_result.filter(date="2021-03-15").order_by('-handwashing_facilities')
        context = {'Covid19': query_result_table, 'script_wash_case': script_wash_case, 'div_wash_case': div_wash_case,
                   'script_wash_death': script_wash_death, 'div_wash_death': div_wash_death}
        return render(request, 'covid19/covid19_handwashing.html', context)
    return render(request, 'covid19/covid19_handwashing.html')


def covid19_hospital_beds(request):
    if request.GET.get("Location") and request.GET.get("start_date"):
        country_filter = request.GET.get("Location")
        date_filter = request.GET.get("start_date")
        if country_filter == "World":
            query_result = Covid19.objects.filter(Q(location="World") & Q(date__gte=date_filter))

        else:
            query_result = Covid19.objects.filter(Q(continent=country_filter) & Q(date__gte=date_filter))

        cases_list = []
        deaths_list = []
        hosp_bed_list = []
        icu_list = []
        hosp_patient_list = []

        for result in query_result:
            cases_list.append(result.total_cases)
            deaths_list.append(result.total_deaths)
            hosp_bed_list.append(result.hospital_beds_per_thousand)
            icu_list.append(result.icu_patients)
            hosp_patient_list.append(result.hosp_patients)

        # Plot scatter plot for covid 19 cases vs Hospital beds per thousand
        x_scatter_hosp_bed = hosp_bed_list
        y_scatter_cases = cases_list

        scatter_plot_bed_case = figure(plot_width=700, plot_height=700,
                                       x_axis_label='Hospital beds per thousand',
                                       y_axis_label='Number of COVID 19 cases in ' + country_filter)
        # scatter_plot_bed_case.circle(x_scatter_hosp_bed, y_scatter_cases, size=10, line_color="navy",
        #                              fill_color="orange",
        #                              fill_alpha=0.5)
        scatter_plot_bed_case.vbar(x_scatter_hosp_bed, width=0.3, bottom=0, top=y_scatter_cases, color="blue")
        scatter_plot_bed_case.left[0].formatter.use_scientific = False
        scatter_plot_bed_case.below[0].formatter.use_scientific = False
        script_bed_case, div_bed_case = components(scatter_plot_bed_case)

        # Plot scatter plot for covid 19 deaths vs Hospital beds per thousand
        x_scatter_hosp_bed = hosp_bed_list
        y_scatter_deaths = deaths_list

        scatter_plot_bed_death = figure(plot_width=700, plot_height=700,
                                        x_axis_label='Hospital beds per thousand',
                                        y_axis_label='Number of COVID 19 deaths in ' + country_filter)
        # scatter_plot_bed_death.circle(x_scatter_hosp_bed, y_scatter_deaths, size=10, line_color="navy",
        #                               fill_color="orange",
        #                               fill_alpha=0.5)
        scatter_plot_bed_death.vbar(x_scatter_hosp_bed, width=0.3, bottom=0, top=y_scatter_deaths, color="orange")
        scatter_plot_bed_death.left[0].formatter.use_scientific = False
        scatter_plot_bed_death.below[0].formatter.use_scientific = False
        script_bed_death, div_bed_death = components(scatter_plot_bed_death)

        # Plot scatter plot for icu patients vs Hospital beds per thousand
        x_scatter_hosp_bed = hosp_bed_list
        y_scatter_icu = icu_list

        scatter_plot_bed_icu = figure(plot_width=700, plot_height=700,
                                      x_axis_label='Hospital beds per thousand',
                                      y_axis_label='Number of COVID 19 patients admitted to ICU in ' + country_filter)
        # scatter_plot_bed_icu.circle(x_scatter_hosp_bed, y_scatter_icu, size=10, line_color="navy",
        #                             fill_color="orange",
        #                             fill_alpha=0.5)
        scatter_plot_bed_icu.vbar(x_scatter_hosp_bed, width=0.3,bottom=0,top=y_scatter_icu,color="red")
        scatter_plot_bed_icu.left[0].formatter.use_scientific = False
        scatter_plot_bed_icu.below[0].formatter.use_scientific = False
        script_bed_icu, div_bed_icu = components(scatter_plot_bed_icu)

        # Plot scatter plot for hospital patients vs Hospital beds per thousand
        x_scatter_hosp_bed = hosp_bed_list
        y_scatter_hos = hosp_patient_list

        scatter_plot_bed_hos = figure(plot_width=700, plot_height=700,
                                      x_axis_label='Hospital beds per thousand',
                                      y_axis_label='Number of COVID 19 patients admitted to ICU in ' + country_filter)
        # scatter_plot_bed_hos.circle(x_scatter_hosp_bed, y_scatter_hos, size=10, line_color="navy",
        #                             fill_color="orange",
        #                             fill_alpha=0.5)
        scatter_plot_bed_hos.vbar(x_scatter_hosp_bed, width=0.3, bottom=0, top=y_scatter_hos,color="black")
        scatter_plot_bed_hos.left[0].formatter.use_scientific = False
        scatter_plot_bed_hos.below[0].formatter.use_scientific = False
        script_bed_hos, div_bed_hos = components(scatter_plot_bed_hos)


        query_result_table = query_result.filter(date="2021-03-15").order_by('-hospital_beds_per_thousand')
        context = {'Covid19': query_result_table, 'script_bed_case': script_bed_case, 'div_bed_case': div_bed_case,
                   'script_bed_death': script_bed_death, 'div_bed_death': div_bed_death,
                   'script_bed_icu': script_bed_icu, 'div_bed_icu': div_bed_icu,
                   'script_bed_hos': script_bed_hos, 'div_bed_hos': div_bed_hos}
        return render(request, 'covid19/covid19_hospital_beds.html', context)
    return render(request, 'covid19/covid19_hospital_beds.html')
