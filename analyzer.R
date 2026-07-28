#!/usr/bin/env Rscript


library(shiny)
library(bslib)
library(dplyr)
library(ggplot2)

df <- read.csv('info.csv')

symbols <- as.list(unique(df$Name))



# Define UI for app that draws a histogram ----
ui <- page_sidebar(
  # App title ----
  title = "Stock market viewer",
  # Sidebar panel for inputs ----
  sidebar = sidebar(
    selectInput(
    "symbol",
    label =  "Select a symbol to view",
    choices = symbols,
    )
  ),
  plotOutput("value_plot"),
)

# Define server logic required to draw a histogram ----
server <- function(input, output) {

  # Histogram of the Old Faithful Geyser Data ----
  # with requested number of bins
  # This expression that generates a histogram is wrapped in a call
  # to renderPlot to indicate that:
  #
  # 1. It is "reactive" and therefore should be automatically
  #    re-executed when inputs (input$bins) change
  # 2. Its output type is a plot

  output$value_plot <- renderPlot({
    
    d <- df %>% filter(Name == input$symbol)
    d <- d %>% mutate(Time = substr(Time, 1, 16)) %>% mutate(Time = as.POSIXct(Time, format = "%Y-%m-%dT%H:%M", tz = "UTC"))
    
    
    ggplot(d, aes(x = Time, y = Price)) +
        geom_line() +
        geom_point() +
        labs(x = "Time", y = "Price")
    })
}

shinyApp(ui = ui, server = server)