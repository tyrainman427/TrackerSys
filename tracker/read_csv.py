import pandas as pd


def get_data(request):
    # df=pd.read_csv(filepath_or_buffer = 'MOCK_DATA.csv')
    # return df
    csvfile = request.FILES['MOCK_DATA.csv']
    data = pd.read_csv(csvfile.name)
    data_html = data.to_html()
    context = {'loaded_data': data_html}
    print("runninggg...")
    return render(request, "tracker/ticket_list.html", context)
