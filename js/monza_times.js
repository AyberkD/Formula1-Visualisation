
function loadAndDisplayMonzaTimes(placement,w,h){
    var margins = {top: 70, right: 50, bottom: 50, left: 70}
    var width = w, height = h
    cy = 18, cx = 15;
    var parseTime = d3.timeParse("%M:%S.%L");
    var formatDate = d3.timeFormat("%M:%S.%L");

    var svg = d3.select(placement).append("svg").attr("viewBox", [0, 0, width, height]);;
    svg.attr("width", width).attr("height", height)
        .append("g")
    var color = d3.scaleOrdinal()
        .range(["#d43d51",
            "#00876c",
            "#8eb87b",
            "#f6e5a2",
            "#eb985f"
            ]);

    d3.csv('./data/monza_2020.csv').then(function(data){
        var count_keys = d3.keys(data[0]).filter(function(key) { return key !== "lapNo"; });
        color.domain(d3.keys(data[0]).filter(function(key) { return key !== "lapNo"; }))

        var laps = color.domain().map(function(name) {
            return {
                name: name,
                values: data.map(function(d) {
                    return {lapNo: d.lapNo, time: parseTime(d[name].replace(/['"]+/g, ''))};
                })
            };
        });

        console.log(d3.min(laps, d => d3.min(d.values, c => c.time)))

        data.forEach(function(d) {
            d.lapNo = +d.lapNo
            return d;
        })

        var x = d3.scaleLinear()
            .rangeRound([margins.left, width - margins.right])
            .domain(d3.extent(data, d => d.lapNo))

        var y = d3.scaleTime()
            .rangeRound([height - margins.bottom, margins.top])
            .domain([d3.min(laps, d => d3.min(d.values, c => +c.time)), d3.max(laps, d => d3.max(d.values, c => +c.time))])

        var z = d3.scaleOrdinal(d3.schemeCategory10);

        var line = d3.line()
            .defined(d => !isNaN(d.time))
            .curve(d3.curveCardinal)
            .x(function(d) { return x(d.lapNo); })
            .y(function(d) { return y(+d.time); });

        svg.append("g")
            .attr("class","x-axis")
            .attr("transform", "translate(0," + (height - margins.bottom) + ")")
            .call(d3.axisBottom(x))

        svg.append("g")
            .attr("class", "y-axis")
            .attr("transform", "translate(" + margins.left + ",0)")
            .call(d3.axisLeft(y).tickFormat(formatDate))
            .call(g => g.select(".tick:last-of-type text").clone()
                .attr("x", 3)
                .attr("text-anchor", "start")
                .attr("font-size", "14px")
                .attr("font-weight", "bold")
                .style("fill", "white")
                .text("Lap  Time"))

        svg.append("g").attr("class", "ChartName")
            .attr("transform", `translate(${(width) / 2 - margins.right - margins.left - (legendWidth+24)},0)`)
            .append("text")
            .attr("font-size", "24px")
            .attr("dy", ".9em")
            .style("text-anchor", "start")
            .text("Top 5 Drivers in 2019 Italian Grand Prix");

        svg.append("g").attr("class", "x-axis-name")
            .attr("transform", `translate(${(width) / 2},${height - 15})`)
            .append("text")
            .attr("font-weight","bold")
            .attr("font-size", "14px")
            .style("text-anchor", "start")
            .style("fill", "white")
            .text("Lap Number");

        var lap = svg.selectAll(".lap")
            .data(laps)
            .enter().append("g")
            .attr("class", "lap");

        var path = lap.append("path")
            .attr("class", function(d) { return "line " + (d.name.replace(/\s/g,'')); })
            .attr("d", function(d) { return line(d.values); })
            .attr("transform", "translate(0," + (-20) + ")")
            .style("stroke", function(d) { return color(d.name); })
            .style("stroke-width", "1px")

        var legend = svg.selectAll(".legend")
            .data(count_keys.slice())
            .enter().append("g")
            .attr("class", "legend")
            .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; })
            .on("click",function(d){
                var thislegend = d3.select(this)
                var driverLine  = svg.select("." + d.replace(/\s/g,'')).style("opacity",1)

                thislegend.classed("selected",!thislegend.classed("selected"))
                driverLine.classed("selected-line",!driverLine.classed("selected-line"))

                svg.selectAll(".legend").style("opacity",0.2)
                svg.selectAll(".selected").style("opacity",1)


                if(svg.selectAll(".selected").size() == 0){
                    svg.selectAll(".legend").style("opacity",1)
                    svg.selectAll(".line").style("opacity",1)
                }

                if(svg.selectAll(".selected-line").size() == 0){
                    svg.selectAll(".line").style("opacity",1)
                }
                else{
                    svg.selectAll(".line").style("opacity",0.05)
                    svg.selectAll(".selected-line").style("opacity",1)
                }

            });

        legend.append("circle")
            .attr("cx", width - cx)
            .attr("cy", cy)
            .attr("r",5)
            .style("fill", color);

        legend.append("text")
            .attr("x", width - 24)
            .attr("y", 17)
            .attr("dy", ".35em")
            .style("text-anchor", "end")
            .text(function(d) { return d; })
            .on("mouseover", function(d, i) {
                if(svg.selectAll(".selected-line").size() == 0) {
                    svg.selectAll(".line").style("opacity", 0.1)
                    svg.select("." + d.replace(/\s/g,'')).style("opacity",1)
                }
            })
            .on('mouseout',function(d) {
                if(svg.selectAll(".selected-line").size() == 0) {
                    svg.selectAll(".line").style("opacity", 1)
                }
            });

    })
}

loadAndDisplayMonzaTimes("#Linechart",((windowSize *0.9)),600)