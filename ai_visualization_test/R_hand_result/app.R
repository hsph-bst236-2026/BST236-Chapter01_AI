library(shiny)
library(bslib)
library(dplyr)
library(readr)
library(ggplot2)
library(plotly)

penguins <- read_csv("penguins.csv", show_col_types = FALSE)

numeric_vars <- c(
  "Bill Length (mm)",
  "Bill Depth (mm)",
  "Flipper Length (mm)",
  "Body Mass (g)"
)

ui <- page_fillable(
  theme = bs_theme(version = 5, bootswatch = "flatly"),
  title = "Penguins Explorer",
  tags$head(
    tags$style(
      HTML(
        ".app-header {padding: 12px 16px; background: #1f6feb; color: white; border-radius: 10px; margin-bottom: 12px;}\n",
        ".sidebar .form-group {margin-bottom: 12px;}\n",
        ".plot-grid {display: grid; grid-template-columns: 1fr 180px; grid-template-rows: 130px 1fr; gap: 10px;}\n",
        ".plot-top {grid-column: 1; grid-row: 1;}\n",
        ".plot-main {grid-column: 1; grid-row: 2;}\n",
        ".plot-right {grid-column: 2; grid-row: 2;}\n",
        ".plot-empty {grid-column: 2; grid-row: 1;}\n"
      )
    )
  ),
  div(
    class = "app-header",
    h2("Interactive Penguin Scatter with Marginals"),
    div("Choose X/Y variables and species to update the plots")
  ),
  layout_sidebar(
    sidebar = sidebar(
      width = 280,
      h4("Controls"),
      selectInput(
        "x_var",
        "X var",
        choices = numeric_vars,
        selected = "Bill Length (mm)"
      ),
      selectInput(
        "y_var",
        "Y var",
        choices = numeric_vars,
        selected = "Bill Depth (mm)"
      ),
      h5("Species"),
      checkboxGroupInput(
        "species",
        label = NULL,
        choices = sort(unique(penguins$Species)),
        selected = unique(penguins$Species)
      )
    ),
    div(
      class = "plot-grid",
      div(class = "plot-top", plotlyOutput("density_x", height = 120)),
      div(class = "plot-empty"),
      div(class = "plot-main", plotlyOutput("scatter_plot", height = 520)),
      div(class = "plot-right", plotlyOutput("density_y", height = 520))
    )
  )
)

server <- function(input, output, session) {
  filtered_data <- reactive({
    req(input$x_var, input$y_var)
    penguins %>%
      filter(Species %in% input$species) %>%
      filter(!is.na(.data[[input$x_var]]), !is.na(.data[[input$y_var]]))
  })

  output$scatter_plot <- renderPlotly({
    df <- filtered_data()
    x_var <- input$x_var
    y_var <- input$y_var

    p <- ggplot(
      df,
      aes(
        x = .data[[x_var]],
        y = .data[[y_var]],
        color = Species,
        text = paste(
          "Species:", Species,
          "<br>Island:", Island,
          "<br>Sex:", Sex,
          "<br>", x_var, ":", .data[[x_var]],
          "<br>", y_var, ":", .data[[y_var]]
        )
      )
    ) +
      geom_point(alpha = 0.8, size = 2.5) +
      theme_minimal(base_size = 12) +
      labs(x = x_var, y = y_var, color = "Species")

    ggplotly(p, tooltip = "text") %>%
      layout(legend = list(orientation = "h", x = 0, y = -0.2))
  })

  output$density_x <- renderPlotly({
    df <- filtered_data()
    x_var <- input$x_var
    p <- ggplot(
      df,
      aes(x = .data[[x_var]], fill = Species, color = Species)
    ) +
      geom_density(alpha = 0.4) +
      theme_minimal(base_size = 11) +
      theme(
        legend.position = "none",
        axis.title.y = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks.y = element_blank()
      ) +
      labs(x = NULL, y = NULL)

    ggplotly(p) %>%
      layout(margin = list(t = 10, r = 10, b = 30, l = 50))
  })

  output$density_y <- renderPlotly({
    df <- filtered_data()
    y_var <- input$y_var
    p <- ggplot(
      df,
      aes(x = .data[[y_var]], fill = Species, color = Species)
    ) +
      geom_density(alpha = 0.4) +
      coord_flip() +
      theme_minimal(base_size = 11) +
      theme(
        legend.position = "none",
        axis.title.x = element_blank(),
        axis.text.x = element_blank(),
        axis.ticks.x = element_blank()
      ) +
      labs(x = NULL, y = NULL)

    ggplotly(p) %>%
      layout(margin = list(t = 10, r = 10, b = 40, l = 10))
  })
}

shinyApp(ui, server)
