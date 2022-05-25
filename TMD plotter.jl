using GLMakie
using Makie
using DifferentialEquations
using ParameterizedFunctions


fig = Figure(resolution=(800, 600))
ax = Axis(fig[1, 1], aspect=1)

lsgrid = labelslidergrid!(
    fig,
    ["Initial pos", "Initial vel", "Stiffness", "Damping", "Mass", "Initial pos 2", "Initial vel 2", "Stiffness 2", "Damping 2", "Mass 2"],
    [-1:0.01:1, -1:0.01:10, 0:0.01:10, 0:0.01:10, 0.1:0.01:10, -1:0.01:1, -1:0.01:1, 0:0.01:2, 0:0.0025:2, 0.1:0.0025:2],
    formats=[x -> "$(round(x, digits=2))$s" for s in ["m", "m/s", "Ns/m", "N/m", "kg", "m", "m/s", "Ns/m", "N/m", "kg"]],
    tellheight=false
)

fig[1, 2] = lsgrid.layout
sliderobservables = [s.value for s in lsgrid.sliders]
x₀₁, v₀₁, k₁, c₁, m₁, x₀₂, v₀₂, k₂, c₂, m₂ = sliderobservables

TMD! = @ode_def begin
    dx₁ = v₁
    dx₂ = v₂
    dv₁ = (-(k₁ + k₂) * x₁ - (c₁ + c₂) * v₁ + k₂ *  x₂ + c₂ * v₂) / m₁
    dv₂ = (k₂ * x₁ + c₂ * v₁ - k₂ * x₂ - c₂ * v₂) / m₂
end k₁ k₂ c₁ c₂ m₁ m₂
tspan = (0, 100)

points = @lift begin
    u₀ = [$x₀₁, $x₀₂, $v₀₁, $v₀₂]
    p = [$k₁, $k₂, $c₁, $c₂, $m₁, $m₂]
    prob = ODEProblem(TMD!, u₀, tspan, p, reltol=1e-14, abstol=1e-14)
    sol = solve(prob, alg=Vern9())
    y = [x[1] for x in sol.u]
    t = sol.t
    Point2f.(t, y)
    #reset_limits!(ax)
end

points2 = @lift begin
    u₀ = [$x₀₁, $x₀₂, $v₀₁, $v₀₂]
    p = [$k₁, $k₂, $c₁, $c₂, $m₁, $m₂]
    prob = ODEProblem(TMD!, u₀, tspan, p, reltol=1e-14, abstol=1e-14)
    sol = solve(prob, alg=Vern9())
    y = [x[2] for x in sol.u]
    t = sol.t
    Point2f.(t, y)
    #reset_limits!(ax)
end

lines!(points, linewidth=5)
lines!(points2)


fig

