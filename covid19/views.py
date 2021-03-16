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
        selected_start_date = datetime.datetime(int(start_date_list[0]), int(start_date_list[1]), int(start_date_list[2]))

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
        i = 0
        j = 0
        print(counter)
        for cases in query_result.values_list('total_cases'):
            if i <= counter:
                cases_list.append(cases)
                i += 1

        for deaths in query_result.values_list('total_deaths'):
            if j <= counter:
                deaths_list.append(deaths)
                j += 1


        print(len(date_list))
        print(len(cases_list))
        print(date_list[0])
        print(date_list[1])


        # Plot the graph of total cases
        month_list = ["January","February","March","April","May","June","July","August","September", "October", "December"]
        plot2 = figure(title="Number of Total cases from " + start_date + " to " + end_date,
                       x_range=month_list,
                       plot_width=800,
                       plot_height=400)
        plot2.left[0].formatter.use_scientific = False
        plot2.vbar(date_list, width=0.5, bottom=0, top=cases_list, color="firebrick")
        #plot2.line(date_list, cases_list, line_width=2)
        script2, div2 = components(plot2)

        # Plot the number of total deaths
        plot3 = figure(title="Number of Total Deaths from " + start_date + " to " + end_date,
                       x_range=date_list,
                       plot_width=800, plot_height=400)
        plot3.left[0].formatter.use_scientific = False
        #plot3.line(date_list, deaths_list, line_width=2)
        plot3.vbar(date_list, width=0.5, bottom=0, top=deaths_list, color="firebrick")
        script3, div3 = components(plot3)

        context = {'Covid19': query_result, 'script2': script2, 'div2': div2, 'script3': script3, 'div3': div3}
        return render(request, 'covid19/query.html', context)

    return render(request, 'covid19/query.html')
