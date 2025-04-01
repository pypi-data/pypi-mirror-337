const output = document.getElementById("output");
const code = document.getElementById("code");

function addToOutput(s) {
  output.value += ">>>" + code.value + "\n" + s + "\n";
}

output.value = "Initializing...\n";

// init Pyodide
async function main() {
  let pyodide = await loadPyodide();
  await pyodide.loadPackage("micropip");
  const micropip = pyodide.pyimport("micropip");
  await micropip.install("boil-an-egg");
  output.value += "Ready!\n";
  return pyodide;
}
let pyodideReadyPromise = main();

//Some funcs
// Equivalent of np.linspace
function linspace(start, stop, num) {
  const step = (stop - start) / (num - 1);
  return Array(num).fill().map((_, i) => start + step * i);
}

function egg_curve_squared(a, b, x_i) {
  return x.map((val) =>
    val * 0.5 *
    ((a - b) - 2 * val + Math.sqrt(4 * b * val + Math.pow(a - b, 2)))
  );
}

// Set up simulation parameters and vars
const EGG_LENGTH_METRES = 7 / 100;
const YOLK_RADIUS_METRES = 1.5 / 100;
const WATER_TEMPERATURE_CELSIUS = 100;
const B = 0.05; // Egg shape parameter
const nx = 10; // Number of grid points
const ny = 10;
const Lx = EGG_LENGTH_METRES; // x domain dimensions = egg length
// y dimension depends on how wide the egg is

const x = linspace(0, Lx, nx);
const y_curve_values = egg_curve_squared(Lx, B, x).map(Math.sqrt);
const Ly = Math.max(...y_curve_values);

// spatial step sizes
const dx = Lx / (nx - 1);
const dy = Ly / (ny - 1);
const tmax = 60 * 5; // total simulation time in seconds
const dt = 1; // timestep in seconds

// Create grid
// x already created above
const y = linspace(0, Ly, ny);

async function evaluatePython() {
  let pyodide = await pyodideReadyPromise;
  try {
    let bae = pyodide.pyimport("boil_an_egg.utils");
    const egg_domain = bae.create_egg_domain(
      nx,
      ny,
      Lx,
      Ly,
      YOLK_RADIUS_METRES,
      B,
    );

    const egg_to_equation_system_map = bae.compute_egg_to_equation_system_map(
      nx,
      ny,
      egg_domain,
    );
    const map_from_mesh_cell_numbers_to_coords = bae
      .map_mesh_cell_numbers_to_coords(
        egg_to_equation_system_map,
      );

    const map_from_coords_to_mesh_cell_numbers = bae.invert_dictionary(
      map_from_mesh_cell_numbers_to_coords,
      true,
    );

    const unstructured_egg_domain = bae
      .create_unstructured_array_from_structured_array(
        egg_domain,
        map_from_mesh_cell_numbers_to_coords,
      );

    const nearest_neighbors = bae.get_nearest_neighbors(
      nx,
      ny,
      map_from_mesh_cell_numbers_to_coords,
      egg_to_equation_system_map,
    );
    const egg_boundary_mesh_cells = bae.get_egg_boundary_mesh_cells(
      nearest_neighbors,
    );

    // Initial condition
    const u_init = new Float64Array(nearest_neighbors.length).fill(273 + 20);
    console.log(u_init);

    const N = u_init.length;
    const nt = Math.floor(tmax / dt) + 1;
    const n_saves = nt;
    // Storage for solution at saved times
    const u_history = Array(n_saves).fill().map(() => Array(N).fill(0));
    const t_saved = Array(n_saves).fill(0);

    // Add initial condition
    let u = [...u_init]; // Create a copy of u_init
    u_history[0] = u;
    t_saved[0] = 0;

    // Main time loop
    let save_idx = 1;
    u = bae.compute_next_u(
      u,
      dt,
      dx,
      dy,
      unstructured_egg_domain,
      nearest_neighbors,
      egg_boundary_mesh_cells,
      WATER_TEMPERATURE_CELSIUS,
    );
    console.log(u);
    // for (let timestep = 1; timestep < nt; timestep++) {
    //   u = bae.compute_next_u({
    //     u: u,
    //     dt: dt,
    //     dx: dx,
    //     dy: dy,
    //     unstructured_egg_domain: unstructured_egg_domain,
    //     nearest_neighbors: nearest_neighbors,
    //     egg_boundary_mesh_cells: egg_boundary_mesh_cells,
    //     water_temperature_celsius: WATER_TEMPERATURE_CELSIUS,
    //   });
    //
    //   u_history[save_idx] = u;
    //   t_saved[save_idx] = timestep * dt;
    //   save_idx++;
    //   addToOutput(timestep);
    // }
  } catch (err) {
    addToOutput(err);
  }
}
