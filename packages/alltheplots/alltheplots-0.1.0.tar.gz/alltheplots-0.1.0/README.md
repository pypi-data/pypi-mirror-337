## alltheplots - Quick & Automatic Plots for All Array Dimensionalities

![GitHub](https://img.shields.io/github/license/gomezzz/alltheplots?style=flat-square)
![GitHub contributors](https://img.shields.io/github/contributors/gomezzz/alltheplots?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/gomezzz/alltheplots?style=flat-square)
![GitHub pull requests](https://img.shields.io/github/issues-pr/gomezzz/alltheplots?style=flat-square)
![CI](https://img.shields.io/github/actions/workflow/status/gomezzz/alltheplots/automated_tests.yml?label=Tests&style=flat-square)

![Alt Text](resources/demo_full.gif)

<p align="left">
    <a href="https://github.com/gomezzz/alltheplots/issues">Report Bug</a>
    ·
    <a href="https://github.com/gomezzz/alltheplots/issues">Request Feature</a>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About the Project</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#examples">Examples</a></li>
    <ul>
        <li><a href="#basic-usage">Basic Usage</a></li>
        <li><a href="#saving-plot-to-file">Saving Plot to File</a></li>
        <li><a href="#custom-theme">Using a Custom Theme</a></li>
        <li><a href="#framework-compatibility">Framework Compatibility</a></li>
        <li><a href="#example-notebooks">Example Notebooks</a></li>
    </ul>
    <li><a href="#dependencies">Dependencies</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About the Project

`alltheplots` provides an extremely simple Python interface for creating quick visualizations from numerical arrays, automatically detecting dimensionality (1D, 2D, 3D, 4D, nD) and providing commonly used plots. 

The core goal of `alltheplots` is to abstract away the plotting details, letting you instantly visualize your data without having to remember specific plot types or parameters. It wraps `seaborn` and `matplotlib`, providing a user-friendly layer which typically sensible default plots.

- **Simple**: Single public `.plot()` function.
- **Automatic**: Detects array dimensionality and chooses appropriate plots automatically.
- **Flexible**: Supports numpy-like arrays from libraries such as `numpy`, `pytorch`, `TensorFlow`, `jax`, and `cupy` seamlessly.
- **Minimal dependencies**: built on top of `matplotlib`, `numpy`, `scipy`, `seaborn`, `scikit-learn`, and `umap-learn`.

## Installation

You can install the latest release using pip:

```bash
pip install alltheplots
```

Alternatively, install directly from source (Git required):

```bash
git clone https://github.com/gomezzz/alltheplots.git
cd alltheplots
pip install -e .
```

## Examples

Below are a few quick examples demonstrating typical usage.

### Basic Usage

Generate standard plots automatically based on the dimensionality of your data.

```python
import numpy as np
from alltheplots import plot

data = np.random.randn(1000)
plot(data)
```

<img src="resources/ex1.png" width="600"/>

### Saving Plot to File

You can easily save plots to file:

```python
plot(data, filename="my_plot.png", dpi=300)
```

### Custom Theme

Users are encouraged to manage the visual style externally by setting global themes in `matplotlib` or `seaborn`. For example:

```python
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="ticks", palette="deep")
plt.style.use("dark_background")

# Then call the plot function
plot(data)
```

<img src="resources/ex2.png" width="600"/>

This approach provides more flexibility and aligns with best practices for managing plot aesthetics.

### Example Notebooks

For more detailed examples, check out the notebooks in the `examples/` directory:

- [1D Examples](https://github.com/gomezzz/alltheplots/blob/main/examples/1D_Examples.ipynb) - Visualizing 1D arrays with time-domain, frequency-domain, and distribution plots
- [2D Examples](https://github.com/gomezzz/alltheplots/blob/main/examples/2D_Examples.ipynb) - Visualizing 2D arrays with heatmaps, contours, and 3D surface plots
- [3D Examples](https://github.com/gomezzz/alltheplots/blob/main/examples/3D_Examples.ipynb) - Visualizing 3D arrays with slice views, projections, and distribution analysis
- [nD Examples](https://github.com/gomezzz/alltheplots/blob/main/examples/nD_Examples.ipynb) - Visualizing high-dimensional arrays with dimensionality reduction techniques

These notebooks provide comprehensive examples of the various visualization capabilities and can help you understand how to best use the library for your specific data.

## Dependencies

- `matplotlib` - Core plotting library
- `numpy` - Array manipulation
- `scipy` - Scientific computing
- `seaborn` - Statistical data visualization
- `scikit-learn` - Machine learning for dimensionality reduction
- `umap-learn` - UMAP dimensionality reduction for high-dimensional data
- `loguru` - Logging

## Contributing

Contributions are welcome! Please open issues and submit PRs at the [GitHub repository](https://github.com/gomezzz/alltheplots).

## License

Distributed under the GPL 3 License. See `LICENSE` for more information.