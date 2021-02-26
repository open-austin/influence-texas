import React, { useState } from 'react'
import { useHistory } from 'react-router-dom'
import { Typography } from '@material-ui/core'
import DonutChart from 'components/DonutChart'
import BillList from 'components/BillList'
import FilterSection from 'components/FilterSection'
import { gql } from 'apollo-boost'
import { getQueryString, dashesToSpaces, getDebugQuery } from 'utils'

const ALL_BILLS = gql`
  query AllBills(
    $chamber: String
    $classification: String
    $party: String
    $multipleSponsors: Boolean
    $first: Int
    $last: Int
    $after: String
    $before: String
  ) {
    bills(
      chamber_Icontains: $chamber
      classification: $classification
      multipleSponsors: $multipleSponsors
      party: $party
      first: $first
      last: $last
      after: $after
      before: $before
    ) {
      totalCount
      pageInfo {
        hasNextPage
        hasPreviousPage
        startCursor
        endCursor
      }
      edges {
        cursor
        node {
          pk
          chamber
          billId
          title
        }
      }
    }
    billClassificationStats(
      chamber: $chamber
      multipleSponsors: $multipleSponsors
      party: $party
    ) {
      name
      count
    }
    ${getDebugQuery()}
  }
`

function BillsPage() {
  document.title = `Bills - Influence Texas`
  const history = useHistory()
  const { page, first, last, before, after, ...queryObj } = getQueryString(
    history,
  )
  const [listData, setListData] = useState()

  const billClassificationStats = listData
    ? listData.billClassificationStats
    : []
  const classificationTags = billClassificationStats.map((d) => ({
    name: dashesToSpaces(d.name),
    value: d.name,
    group: 'classification',
  }))
  const summaryData =
    listData &&
    billClassificationStats.map((d) => ({
      name: dashesToSpaces(d.name),
      value: d.count,
    }))

  return (
    <div>
      <FilterSection
        title={<Typography variant="h6">Texas Bills</Typography>}
        tags={{
          chamber: [
            { name: 'House', value: 'HOUSE' },
            { name: 'Senate', value: 'SENATE' },
          ],
          party: [
            { name: 'Republican', value: 'R' },
            { name: 'Bipartisan', value: 'Bipartisan' },
            { name: 'Democratic', value: 'D' },
          ],
          multipleSponsors: [{ name: 'Many Sponsors', value: true }],
          classification: classificationTags,
        }}
      />
      <div className="two-column">
        <DonutChart
          data={summaryData}
          totalCount={listData ? listData.bills.totalCount : 0}
          totalText="Bills"
          selectedSlice={dashesToSpaces(queryObj.classification)}
          loading={!listData}
        />
        <BillList
          gqlQuery={ALL_BILLS}
          gqlVariables={queryObj}
          title="All Bills"
          onDataFetched={setListData}
        />
      </div>
    </div>
  )
}

export default BillsPage
