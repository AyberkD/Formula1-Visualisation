


    function loadAndDisplayWinPodiumCount(placement,w,h){
        var margins = {top: 50, right: 50, bottom: 50, left: 50}, barWidth = 30, barOffset = 5;
        var width = w - margins.left - margins.right, height = h - margins.top - margins.bottom
        legendWidth = 18, legendHeight = 18;


        var color = d3.scaleOrdinal()
            .range(["#28593D","#D37385"]);

        var x0 = d3.scaleBand()
            .rangeRound([margins.left, width ])
            .padding(0.25);

        var x1 = d3.scaleBand();

        var y = d3.scaleLinear()
            .range([height - margins.top, margins.bottom]);
        var xAxis = d3.axisBottom()
            .scale(x0);
        var yAxis = d3.axisLeft()
            .scale(y)
            .tickSizeInner(width - margins.left)
            .tickFormat(d3.format(".2s"));

        var tooltip = d3.select(placement).append('div')
            .attr("class", "tooltip")
            .style('position','absolute')
            .style('padding','0 10px')
            .style('opacity',0)


        var svg = d3.select(placement).append("svg");
        svg.attr("width", width).attr("height", height)
            .append("g")


        d3.csv('./data/win_and_podium_statistics.csv').then(function(data) {
            var count_keys = d3.keys(data[0]).filter(function(key) { return key !== "Name"; });
            var names = d3.keys(data[0]).filter(function(key){ return key == "Name"})

            data.forEach(function(d){
                d.driver_success = count_keys.map(function(name) { return {name: name, value: +d[name]}; });
            })
            x0.domain(data.map(function(d) { return d.Name; }));
            x1.domain(count_keys).rangeRound([0, x0.bandwidth()]);
            y.domain([0, d3.max(data, function(d) { return d3.max(d.driver_success, function(d) { return d.value + 5; }); })]);

            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", `translate(0,${height - margins.bottom})`)
                .call(xAxis);

            svg.append("g").attr("class", "BarName")
                .attr("transform", `translate(${(width) / 2 - margins.right - margins.left - (legendWidth+24)},0)`)
                .append("text")
                .attr("font-size", "24px")
                .attr("dy", ".9em")
                .style("text-anchor", "center")
                .text("F1 Best Drivers by Count");

            svg.append("g")
                .attr("class", "y axis")
                .attr("transform", `translate(${width },0)`)
                .attr("position","relative")
                .attr("z-index","-1")
                .attr("dy", "0.32em")
                .call(yAxis)


            var forename = svg.selectAll(".forename")
                .data(data)
                .enter().append("g")
                .attr("class", "Name")
                .attr("transform", function(d) { return "translate(" + x0(d.Name) + ",0)"; });
            forename.selectAll("rect")
                .data(function(d) { return d.driver_success; })
                .enter().append("rect").attr("width", x1.bandwidth())
                .attr("x", function(d) { return x1(d.name); })
                .attr("y", function(d) { return y(d.value); })
                .attr("height", function(d) { return height - margins.bottom - y(d.value); })
                .on("mouseover", function(d, i) {
                    tooltip.transition().duration(1000).style('opacity',0.9)
                    tooltip.style("left", d3.event.pageX-35+"px")
                    .style("top", d3.event.pageY-30+"px")
                        .style('opacity',0)
                    .html(d.value);
                    d3.select(this).style('opacity',0.5)
                })
                .on('mouseout',function(d){
                    d3.select(this).style('opacity',1)
                    tooltip.transition().style('opacity',0)
                })
                .style("fill", function(d) { return color(d.name); });

            var legend = svg.selectAll(".legend")
                .data(count_keys.slice())
                .enter().append("g")
                .attr("class", "legend")
                .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

            legend.append("rect")
                .attr("x", width - legendWidth)
                .attr("width", legendWidth)
                .attr("height", legendHeight)
                .style("fill", color);

            legend.append("text")
                .attr("x", width - 24)
                .attr("y", 9)
                .attr("dy", ".35em")
                .style("text-anchor", "end")
                .text(function(d) { return d; });
        });

    }

var windowSize = screen.width;
loadAndDisplayWinPodiumCount("#Barchart",((windowSize *0.9) / 2),500)
