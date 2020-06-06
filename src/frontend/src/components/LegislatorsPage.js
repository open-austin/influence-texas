import React from 'react'
import { useHistory } from 'react-router-dom'
import { Typography } from '@material-ui/core'
import { gql } from 'apollo-boost'
import { getQueryString, getDebugQuery } from 'utils'
import TexasDistrictMap from 'components/TexasDistrictMap'
import FilterSection from 'components/FilterSection'
import LegislatorList from 'components/LegislatorList'

const ALL_LEG = gql`
  query Legislator(
    $chamber: String
    $party: String
    $first: Int
    $last: Int
    $after: String
    $before: String
  ) {
    legislators(
      party: $party
      chamber_Icontains: $chamber
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
          name
          party
          chamber
          district
          photoUrl
        }
      }
    }
    ${getDebugQuery()}
  }
`

function LegislatorsPage() {
  document.title = `Legislators - Influence Texas`
  const history = useHistory()
  const queryObj = getQueryString(history)

  const chamber = queryObj.chamber
  const party = queryObj.party

  return (
    <div>
      <FilterSection
        title={<Typography variant="h6">Texas Legislators</Typography>}
        tags={{
          chamber: [
            { name: 'House', value: 'HOUSE' },
            { name: 'Senate', value: 'SENATE' },
          ],
          party: [
            { name: 'Democrat', value: 'D' },
            { name: 'Republican', value: 'R' },
          ],
        }}
      />
      <div className="two-column">
        <TexasDistrictMap chamber={chamber} style={{ flexGrow: 1 }} />
        <LegislatorList
          title={'All Legislators'}
          gqlQuery={ALL_LEG}
          gqlVariables={{ chamber, party }}
        />
      </div>
    </div>
  )
}

export default LegislatorsPage
