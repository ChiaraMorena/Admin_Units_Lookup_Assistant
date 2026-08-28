from shiny import App, ui, render
from fun import get_fao_gaul,find_row_by_code,find_row_by_text
import shinyswatch


levels = {'Levels': {0:'0-Country', 1:'1-State', 2:'2-Region'}}

# UI logic

app_ui = ui.page_fluid(
    ui.row(
        ui.column(8,
            ui.div(
            ui.markdown(
                "#### **FAO GAUL LOOKUP ASSISTANT**\n\n\n"
                "###### This tool allows you to create lookups tables for FAO GAUL databases.\n\n" 
                "You can search for a specific location using its administrative unite **code** OR **name**."
                "Both the **2024** and **2015** versions of the FAO GAUL dataset are available for search."
                "You can only specify one level *(0-Country, 1-State, 2-Region)* to search at."
                "If you look for a code the table will show you the exact match, while if you look for a name the table will show you the best matches based on fuzzy matching.\n\n"
                "The results will be displayed in a table below.\n\n\n "
                ),
            style="text-align: justify; line-height: 1.1;",
        ),
            ui.input_text("query", "Query:", "312"),
            ui.markdown("<small> Sources: [Global Administrative Unit Layers (GAUL 2015)](https://data.apps.fao.org/catalog/dataset/global-administrative-unit-layers-gaul-2015) and [Global Administrative Unit Layers (GAUL 2024)](https://data.apps.fao.org/catalog/dataset/global-administrative-unit-layers-gaul-2024)</small>")
        ),
        ui.column(4,
            ui.card(
                ui.h4("SEARCH OPTIONS", style="font-size: 1rem;"),
                ui.row(
                    ui.column(6,
                        ui.input_radio_buttons(
                            "fao_gaul_version",
                            "Version:",
                            {
                                "fao_gaul24": ui.span("2024"),
                                "fao_gaul15": ui.span("2015"),
                            },
                        ),
                    ),
                    ui.column(6,
                        ui.input_radio_buttons(
                            "search_type",
                            "Search by:",
                            {
                                "code": ui.span("Code"),
                                "text": ui.span("Text"),
                            }
                        ),
                    ),
                class_="g-0",
                ),
                ui.input_selectize(
                    "Levels",
                    "Level",
                    levels['Levels'],
                    multiple=False,
                ),
                style="font-size: 1em; padding: 10px; overflow-x: hidden;"
            )
        ),
    ),
    ui.row(ui.column(12, ui.output_data_frame("table"))),
    theme=shinyswatch.theme.sandstone(),
)

# Server logic
def server(input, output, session):

    @render.data_frame
    def table():
        versions = input.fao_gaul_version() 
        fao_gaul_db = get_fao_gaul(versions)
        if input.search_type() == "code" and not input.query().isdigit():
            ui.notification_show(
                            f'Invalid code "{input.query()}". Please enter a valid integer code or change the search options.',
                            type="error",
                            duration=5000,
                        )
            return None
        elif input.search_type() == "text" and input.query().isdigit():
            ui.notification_show(
                f'Invalid text "{input.query()}". Please enter a valid text query or change the search options.',
                type="error",
                duration=5000,
            )
            return None
        elif input.search_type() == "code":
            shown_db = find_row_by_code(fao_gaul_db, input.query(), input.Levels())
            return render.DataGrid(shown_db)
        elif input.search_type() == "text":
            shown_db = find_row_by_text(fao_gaul_db, input.query(), input.Levels())
            return render.DataGrid(shown_db)

# wrap the app
app = App(app_ui, server)