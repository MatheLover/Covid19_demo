import time
from math import pi

from django.shortcuts import render

from datetime import datetime
import datetime
from .models import Covid19
from django.db.models import Q

from bokeh.embed import components
from bokeh.plotting import figure


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
        plot6 = figure(title="Number of COVID 19 Patients Admitted into hospitals from " + start_date + " to " + end_date,
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
    if request.GET.get("location") and request.GET.get("start_date"):
        location_filter = request.GET.get("Location")
        start_date = request.GET.get("start_date")
        query_result = Covid19.objects.filter(Q(location=location_filter) & Q(date=start_date))
    return render(request, 'covid19/covid19_day_stat.html')


def covid19_day_stat_map(request):
    return render(request, 'covid19/covid19_day_stat_map.html')


def covid19_public_health_authority_response(request):
    return render(request, 'covid19/covid19_public_health_authority_response.html')


def covid19_public_health_facility(request):
    return render(request, 'covid19/covid19_public_health_facility.html')


def covid19_public_health_statistics(request):
    return render(request, 'covid19/covid19_public_health_statistics.html')


def covid19_socioeconomic_factor(request):
    return render(request, 'covid19/covid19_socioeconomic_factor.html')
