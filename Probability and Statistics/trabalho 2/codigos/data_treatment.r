library(stringr) # For string manipulation (e.g., str_match, str_split, str_count)
library(dplyr)   # For data manipulation (e.g., mutate, select, rename)
library(tidyr)   # For data tidying (e.g., separate_rows)

# --- 1. Define the Dimension Parsing Function ---
# This function extracts and formats dimensions (e.g., "32.7 x 32.7" or "32.4 x 11.4 x 17.8")
parse_dimensions <- function(dim_string) {
  # Attempt to find dimensions in the format (NUM x NUM cm) or (NUM x NUM x NUM cm)
  pattern_combined <- "\\((\\d+\\.?\\d*)\\s*[x×]\\s*(\\d+\\.?\\d*)(?:\\s*[x×]\\s*(\\d+\\.?\\d*))?\\s*cm\\)"
  match_combined <- str_match(dim_string, pattern_combined)
  
  if (!is.na(match_combined[1, 1])) {
    # If a combined pattern is found, extract and format the numerical dimensions.
    dims <- na.omit(match_combined[1, 2:length(match_combined)])
    return(paste(dims, collapse = " x "))
  }
  
  # If no combined pattern, try to find individual (NUM cm) for H, W, D, etc.
  pattern_individual_cm <- "\\(\\s*(\\d+\\.?\\d*)\\s*cm\\)"
  all_individual_cm_matches <- str_extract_all(dim_string, pattern_individual_cm)[[1]]
  
  if (length(all_individual_cm_matches) > 0) {
    # Extract only the numbers from these matches.
    extracted_nums <- str_replace_all(all_individual_cm_matches, pattern_individual_cm, "\\1")
    # Take up to the first 3 dimensions (assuming H, W, D order for sculptures).
    extracted_nums <- head(extracted_nums, 3)
    return(paste(extracted_nums, collapse = " x "))
  }
  
  # If no relevant pattern is found, return NA.
  return(NA_character_)
}

# --- 2. Load the Original Dataset ---
# Ensure 'tabela_met.csv' is in your R working directory, or provide the full path.
# Example: tabela_met_original <- read.csv("C:/Users/YourUser/Documents/tabela_met.csv")
tabela_met_original <- read.csv("tabela_met.csv") %>%
  # Select only the required columns as they appear in the CSV (using backticks for names with dots).
  select(`Is.Highlight`, `Object.Begin.Date`, Tags, Dimensions) %>%
  # Rename columns for consistency (replacing dots with underscores, maintaining capitalization).
  rename(
    Is_Highlight = `Is.Highlight`,
    Object_Begin_Date = `Object.Begin.Date`
  )

# --- 3. Process Dimensions, Is_Sculpture, and Area/Volume for 'met_data' ---
# This block applies the dimension parsing, replaces the original column,
# adds the 'Is_Sculpture' binary flag, and calculates 'area/volume'.

met_data <- tabela_met_original %>%
  # Apply the parsing function to create a temporary 'parsed_dimensions' column.
  mutate(parsed_dimensions = sapply(Dimensions, parse_dimensions, USE.NAMES = FALSE)) %>%
  # Overwrite the original 'Dimensions' column with the parsed values.
  mutate(Dimensions = parsed_dimensions) %>%
  # Remove the temporary 'parsed_dimensions' column.
  select(-parsed_dimensions) %>%
  # Add the 'Is_Sculpture' column: TRUE if 3 dimensions (two 'x' separators), FALSE otherwise.
  # Handles NA values in 'Dimensions' by setting 'Is_Sculpture' to FALSE.
  mutate(
    Is_Sculpture = ifelse(
      is.na(Dimensions),
      FALSE,
      str_count(Dimensions, "x") == 2
    )
  ) %>%
  # Calculate 'area/volume': product of dimensions. NA if Dimensions is NA.
  mutate(
    `area/volume` = if_else(
      is.na(Dimensions),
      NA_real_, # Return numeric NA if Dimensions is NA.
      sapply(Dimensions, function(d_str) {
        # Split the dimension string into numeric values and calculate their product.
        dims_numeric <- as.numeric(str_split(d_str, " x ")[[1]])
        prod(dims_numeric)
      }, USE.NAMES = FALSE)
    )
  )

# --- 4. Expand 'Tags' Column for 'met_data_tags' ---
# This block takes the 'met_data' (which has the corrected Dimensions, etc.)
# and expands the 'Tags' column so each tag gets its own row.

met_data_tags <- met_data %>%
  # Split the 'Tags' column by the pipe '|' delimiter, creating new rows for each tag.
  # Handles cases where 'Tags' might be NA, producing NA in the expanded rows.
  separate_rows(Tags, sep = "\\|")

write.csv(met_data, "met_data.csv", row.names = FALSE)
write.csv(met_data_tags, "met_data_tags.csv", row.names = FALSE)
