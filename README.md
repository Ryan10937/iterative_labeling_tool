# iterative_labeling_tool




Roadmap:
  Create a "display" abstraction that takes the label and media and displays it on the page
    this is a stretch goal to include other types of media

        

  Train model on dataset
    Select model architecture (or pretrained)
    "train_model" button
    progress bar
    display results
    display worst-performing cases and its model output on those data items
    allow for relabel
    retrain

  
Create New Dataset
1. Set dataset generator config's fields 
1. Make transformation function in transformation_functions to load labels

1. Set iterative labeling config's fields 
1. Make relabeling function  in relabeling_functs to save label 