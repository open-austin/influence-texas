import React, { useState } from 'react'
import { useHistory } from 'react-router-dom'
import { gql } from 'apollo-boost'
import { Typography } from '@material-ui/core'
import DonorList from 'components/DonorList'
import DonutChart from 'components/DonutChart'
import FilterSection from 'components/FilterSection'
import { getQueryString, getDebugQuery } from 'utils'

const ALL_DONORS = gql`
  query AllDonors(
    $first: Int
    $last: Int
    $after: String
    $before: String
    $inState: Boolean
  ) {
    donors(
      first: $first
      last: $last
      after: $after
      before: $before
      inState: $inState
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
          fullName
          city
          state
          employer
          totalContributions
        }
      }
    }
    ${getDebugQuery()}
  }
`

function DonorsPage() {
  document.title = `Donors - Influence Texas`
  const [listData, setListData] = useState()
  const history = useHistory()
  const { page, first, last, before, after, ...queryObj } = getQueryString(
    history,
  )

  const summaryData = [
    { name: 'donors', value: listData ? listData.donors.totalCount : 1 },
  ]

  let selectedSlice
  if (typeof queryObj.inState === 'boolean') {
    if (queryObj.inState) {
      selectedSlice = 'In State'
    } else {
      selectedSlice = 'Out Of State'
    }
  }
  return (
    <div>
      <FilterSection
        title={
          <Typography variant="h6" style={{ minWidth: '150px' }}>
            Texas Donors
          </Typography>
        }
        tags={{
          inState: [
            { name: 'In state', value: true },
            { name: 'Out of state', value: false },
          ],
        }}
      />
      <div className="two-column">
        <DonutChart
          data={summaryData}
          totalCount={listData ? listData.donors.totalCount : 0}
          totalText={'Donors'}
          selectedSlice={selectedSlice}
          loading={!listData}
        />
        <DonorList
          gqlQuery={ALL_DONORS}
          title="Donors"
          onDataFetched={setListData}
          gqlVariables={queryObj}
        />
      </div>
    </div>
  )
}

export default DonorsPage
