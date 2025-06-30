import plotly.graph_objects as go
from scripts.clustering import run_dbscan
from utils.rich_tabulate import rich_tablulate
from utils.tabulate_dir import tabulate_files
from rich.console import Console
from rich.prompt import IntPrompt
from rich.table import Table

console = Console()


def visualize_clusters():
    csv_dir = "data/traffic_csv"
    all_files = tabulate_files(csv_dir, "csv")[0]
    rich_tablulate(all_files)

    try:
        input_index = IntPrompt.ask(
            "Select the index of the file to Visualize Scatter Plot")
    except (ValueError, KeyboardInterrupt):
        console.print(
            "[bold red]No input provided or invalid input. Exiting...[/bold red]")
        return

    if input_index is None or input_index >= len(all_files):
        console.print(
            "[bold red]Invalid index selected. Exiting...[/bold red]")
        return

    input_file = all_files[input_index]
    region_name = input_file.split(
        "/")[-1].split(".")[0].split("_")[0].capitalize()
    console.print(f"[bold yellow]Selected Region:[/bold yellow] {region_name}")

    eps = 0.05
    with console.status("[bold green]Running DBSCAN clustering...[/bold green]"):
        df = run_dbscan(input_file, eps=eps, min_samples=5)

    if 'cluster' not in df.columns:
        console.print(
            "[bold red]DBSCAN failed to produce 'cluster' column. Exiting...[/bold red]")
        return

    labels = df['cluster']
    cluster_counts = labels.value_counts().sort_index()

    largest_cluster = cluster_counts.idxmax()
    top_three_clusters = cluster_counts.nlargest(3).index.tolist()
    smallest_cluster = cluster_counts.idxmin()
    num_clusters = len(cluster_counts) - (1 if -1 in cluster_counts else 0)
    num_noise = (labels == -1).sum()

    stats_table = Table(
        title="[bold]Cluster Statistics[/bold]", show_lines=True)
    stats_table.add_column("Metric", style="bold cyan")
    stats_table.add_column("Value", style="yellow")

    stats_table.add_row("Largest Cluster",
                        f"{largest_cluster} ({cluster_counts.max()} points)")
    stats_table.add_row("Top 3 Clusters", ", ".join(
        map(str, top_three_clusters)))
    stats_table.add_row("Smallest Cluster",
                        f"{smallest_cluster} ({cluster_counts.min()} points)")
    stats_table.add_row("Number of Clusters", str(num_clusters))
    stats_table.add_row("Noise Points", str(num_noise))

    console.print("")  # spacer
    console.print(stats_table)

    bbox_table = Table(
        title="[bold]Top 3 Bounding Boxes[/bold]", show_lines=True)
    bbox_table.add_column("Rank", style="bold magenta")
    bbox_table.add_column("Cluster", style="bold green")
    bbox_table.add_column("Bounding Box", style="cyan")

    for idx, label in enumerate(top_three_clusters, 1):
        cluster_data = df[df['cluster'] == label]
        min_lon, max_lon = cluster_data['lon'].min(), cluster_data['lon'].max()
        min_lat, max_lat = cluster_data['lat'].min(), cluster_data['lat'].max()
        bbox_str = f"(min_lon={min_lon:.5f}, min_lat={min_lat:.5f}, max_lon={max_lon:.5f}, max_lat={max_lat:.5f})"
        bbox_table.add_row(str(idx), str(label), bbox_str)

    console.print("")  # spacer
    console.print(bbox_table)

    mapbox_access_token = None

    fig = go.Figure(layout=dict(mapbox=dict(style="open-street-map")))
    sorted_labels = cluster_counts.sort_values(ascending=False).index.tolist()

    import itertools

    colors = itertools.cycle([
        "blue", "red", "green", "orange", "purple", "cyan", "magenta", "lime", "brown", "pink"
    ])

    for label in sorted_labels:
        cluster_data = df[df['cluster'] == label]
        min_lon, max_lon = cluster_data['lon'].min(), cluster_data['lon'].max()
        min_lat, max_lat = cluster_data['lat'].min(), cluster_data['lat'].max()
        color = next(colors)
        fig.add_trace(go.Scattermap(
            lon=[min_lon, max_lon, max_lon, min_lon, min_lon],
            lat=[min_lat, min_lat, max_lat, max_lat, min_lat],
            mode='lines',
            line=dict(color=color, width=2),
            name=f'Cluster {label}',
            showlegend=True
        ))

    bbox_areas = {}
    for label in sorted_labels:
        if label == -1:
            continue
        cluster_data = df[df['cluster'] == label]
        min_lon, max_lon = cluster_data['lon'].min(), cluster_data['lon'].max()
        min_lat, max_lat = cluster_data['lat'].min(), cluster_data['lat'].max()
        area = (max_lon - min_lon) * (max_lat - min_lat)
        bbox_areas[label] = area

    if bbox_areas:
        largest_bbox_label = max(bbox_areas, key=bbox_areas.get)
        print(
            f"- Largest Bounding Box: Cluster {largest_bbox_label} with area {bbox_areas[largest_bbox_label]:.6f}")

    fig.update_layout(
        title="DBSCAN Clustering (Bounding Boxes Only)",
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=df['lat'].mean(), lon=df['lon'].mean()),
            zoom=5
        ),
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        showlegend=True
    )
    fig.update_geos(visible=False)

    fig.show()


def main():
    visualize_clusters()


if __name__ == "__main__":
    main()
