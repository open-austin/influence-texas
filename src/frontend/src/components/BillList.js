import React from 'react'
import { format } from 'date-fns'
import PaginatedList from './PaginatedList'
import { BillSquare } from '../styles'

function BillList({ data, ...props }) {
  return (
    <PaginatedList
      {...props}
      url="bills/bill"
      data={data}
      emptyState={<div>No bills found</div>}
      columns={[
        {
          render: (rowData) => <BillSquare billId={rowData.node.billId} />,
        },
        {
          render: (rowData) => (
            <div>
              {rowData.node.actionDates && (
                <div style={{ float: 'right', textAlign: 'right' }}>
                  {format(
                    new Date(rowData.node.actionDates.edges[0].node.date),
                    `MMM d`,
                  )}
                  <div>
                    {format(
                      new Date(rowData.node.actionDates.edges[0].node.date),
                      `yyy`,
                    )}
                  </div>
                </div>
              )}
              <span style={{ opacity: 0.5 }}>Relating to</span>
              {rowData.node.title.replace('Relating to', '')}
            </div>
          ),
        },
      ]}
    />
  )
}

export default BillList
