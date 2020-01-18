import React from "react";
import styled from "styled-components";
import { PieChart, Pie, Tooltip, Cell } from "recharts";
import { scaleQuantize } from "d3-scale";
import { numberWithCommas } from "../utils";
import { legTheme } from "../theme";

const Wrapper = styled.div`
  .large {
    font-size: 50px;
    font-weight: bold;
  }
  .recharts-default-legend {
    margin-top: 50px !important;
  }
  .recharts-wrapper {
    margin: auto;
  }
`;

/**
 * @typedef {Object} Props
 * @property {Array<{ name: string, color: string, value: number}>} data - slices of the chart
 * @property {Number} totalCount - Total for middle
 */

/**
 * @param {Props} props
 */
function DonutChart({ data, totalCount = 0 }) {
  const CHART_WIDTH = 440;
  const colorScale = scaleQuantize()
    .domain([1, data.length])
    .range([legTheme.palette.primary.main, legTheme.palette.primary.dart]);
  return (
    <Wrapper>
      <PieChart width={CHART_WIDTH} height={CHART_WIDTH}>
        <Pie
          data={data}
          cx={CHART_WIDTH / 2}
          cy={CHART_WIDTH / 2}
          innerRadius={180}
          outerRadius={200}
          paddingAngle={2}
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={colorScale(index)} />
          ))}
        </Pie>
        <text x={CHART_WIDTH / 2} y={CHART_WIDTH / 2 + 20} textAnchor="middle">
          <tspan className="large">{numberWithCommas(totalCount)}</tspan> Total
          Bills
        </text>
        <Tooltip />
      </PieChart>
    </Wrapper>
  );
}

export default DonutChart;
