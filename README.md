# nyc-events

This project pulls data from a listing of New York City permitted events from https://public.enigma.com/datasets/f93ffd80-6679-4a76-a86e-2ab1f4007815
    supplements the dataset with coordinates given the unstructured event location provided by the city.

## Make the dataset

```bash
export ENGIMA_API_KEY=<YOUR_API_KEY>
export GOOGLE_API_KEY=<YOUR_API_KEY>
make dataset
```

## Make the graph

```bash
make graphs
```
