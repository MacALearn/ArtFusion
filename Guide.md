

## Weights


If the content and style have similar color schemes, use total_variation_weight = 1E-5
If the content and style have at least one major color similar, use total_variation_weight = 5E-05
If the content and style have the same background color, use total_variation_weight = 8E-05
If the content and style do not share same color palette at all, use total_variation_weight = 5E-05
If you want relatively crisp images without worrying about color similarity, use total_variation_weight = 8.5E-05.
   It works well almost 90 % of the time.
If style image is "The Starry Night", use total_variation_weight = 1E-04 or 1E-05. Other values produce distortions
   and unpleasant visual artifacts in most cases.
I have tried turing off total_variation_weight to 0, however the results were very poor. Image produced is sharp,
  but lacks continuity and is not visually pleasing.
  If you want very crisp images at the cost of some continuity in the final image, use total_variation_weight = 5E-08.