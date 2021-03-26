import React from 'react'
import styled from 'styled-components'
import { PieChart, Pie, Tooltip, Cell } from 'recharts'
import { numberWithCommas } from 'utils'
import { useTheme } from '@material-ui/core'

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
`

/**
 * @typedef {Object} Props
 * @property {Array<{ name: string, color: string, value: number}>} data - slices of the chart
 * @property {Number} totalCount - Total for middle
 */

/**
 * @param {Props} props
 */
function DonutChart({
  data = [{ name: 'loading', value: 100 }],
  totalCount = 0,
  totalText = 'Total',
  selectedSlice = '',
  loading,
}) {
  const CHART_WIDTH = Math.min(440, window.innerWidth - 50)
  const props = {
    data,
    cx: CHART_WIDTH / 2,
    cy: CHART_WIDTH / 2,
    paddingAngle: 2,
    dataKey: 'value',
  }
  const { palette } = useTheme()
  return (
    <Wrapper>
      <PieChart width={CHART_WIDTH} height={CHART_WIDTH}>
        <Pie
          {...props}
          innerRadius={CHART_WIDTH / 2 - 30}
          outerRadius={CHART_WIDTH / 2 - 10}
          fill={palette.primary.main}
        >
          {data.map((entry, index) => {
            return (
              <Cell
                key={`cell-${index}`}
                fill={entry.name === selectedSlice ? '#ccc' : 'white'}
              />
            )
          })}
        </Pie>
        <Pie
          {...props}
          innerRadius={CHART_WIDTH / 2 - 30}
          outerRadius={CHART_WIDTH / 2 - 10}
          fill={loading ? '#ccc' : palette.primary.main}
        ></Pie>

        <text x={CHART_WIDTH / 2} y={CHART_WIDTH / 2 + 20} textAnchor="middle">
          {loading ? (
            'loading'
          ) : (
            <>
              <tspan className="large">{numberWithCommas(totalCount)} </tspan>{' '}
              {totalText}
            </>
          )}
        </text>
        <Tooltip />
      </PieChart>
    </Wrapper>
  )
}

export default DonutChart
