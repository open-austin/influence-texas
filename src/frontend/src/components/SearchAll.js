import React, { useState, useEffect } from 'react'
import { Input, InputAdornment } from '@material-ui/core'
import Search from '@material-ui/icons/Search'
import { useQuery } from '@apollo/react-hooks'
import { gql } from 'apollo-boost'
import BillList from 'components/BillList'
import DonorList from 'components/DonorList'
import LegislatorList from 'components/LegislatorList'
import SimpleTabs from 'components/SimpleTabs'
import { useHistory, useParams } from 'react-router-dom'
import CustomLink from 'components/CustomLink'
import useDebounce from 'components/useDebounce'
import { getDebugQuery, getQueryString } from 'utils'

const ALL_SEARCH = gql`
  query SearchAll($searchQuery: String) {
    search(searchQuery: $searchQuery) {
      legislators {
        totalCount
      }
      bills {
        totalCount
      }
      donors {
        totalCount
      }
    }
    _debug {
      sql {
        duration
        sql
      }
    }
  }
`

const LEG_SEARCH = gql`
  query LegislatorSearch(
    $first: Int
    $last: Int
    $after: String
    $before: String
    $searchQuery: String
  ) {
    search(searchQuery: $searchQuery) {
      legislators(
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
    }
    ${getDebugQuery()}
  }
`

const BILL_SEARCH = gql`
  query BillsSearch(
    $first: Int
    $last: Int
    $after: String
    $before: String
    $searchQuery: String
  ) {
    search(searchQuery: $searchQuery) {
      bills(
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
    }
    ${getDebugQuery()}
  }
`

const DONOR_SEARCH = gql`
  query DonorsSearch(
    $first: Int
    $last: Int
    $after: String
    $before: String
    $searchQuery: String
  ) {
    search(searchQuery: $searchQuery) {
      donors(
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
            fullName
            city
            state
            employer
            employerId
            occupation
            totalContributions
          }
        }
      }
    }
    ${getDebugQuery()}
  }
`

export function SearchResults() {
  const { searchQuery } = useParams()
  const history = useHistory()
  const { tab } = getQueryString(history)
  const gqlVariables = { searchQuery: searchQuery || '---' }
  const { data, loading, error } = useQuery(ALL_SEARCH, {
    variables: gqlVariables,
  })
  if (error) {
    return 'server error'
  }
  if (loading) {
    return 'loading'
  }

  let startTabIdx
  if (tab === undefined) {
    // active tab choice should be honored on back
    if (!data.search.legislators.totalCount) {
      startTabIdx = 1
      if (!data.search.bills.totalCount) {
        startTabIdx = 2
        if (!data.search.donors.totalCount) {
          startTabIdx = 0
        }
      }
    }
  }
  return (
    <div className="detail-page">
      {searchQuery && data && <CustomLink to="/"> ← Clear Search</CustomLink>}
      {searchQuery && data && (
        <SimpleTabs
          saveToUrl
          startTabIdx={startTabIdx}
          tabs={[
            {
              label: `Legislators (${data.search.legislators.totalCount})`,
              content: (
                <div>
                  <LegislatorList
                    gqlVariables={gqlVariables}
                    gqlQuery={LEG_SEARCH}
                    nestedUnder="search.legislators"
                  />
                </div>
              ),
            },
            {
              label: `Bills (${data.search.bills.totalCount})`,
              content: (
                <div>
                  <BillList
                    gqlVariables={gqlVariables}
                    gqlQuery={BILL_SEARCH}
                    nestedUnder="search.bills"
                  />
                </div>
              ),
            },
            {
              label: `Donors (${data.search.donors.totalCount})`,
              content: (
                <div>
                  <DonorList
                    gqlVariables={gqlVariables}
                    gqlQuery={DONOR_SEARCH}
                    nestedUnder="search.donors"
                  />
                </div>
              ),
            },
          ]}
        />
      )}
    </div>
  )
}

function SearchAll() {
  document.title = 'Search - Influence Texas'
  const history = useHistory()
  const searchQuery = history.location.pathname.split('/searchAll/')[1]
  const [searchVal, setSearchVal] = useState(searchQuery)
  useEffect(() => {
    setSearchVal(searchQuery)
  }, [searchQuery])
  const debouncedSearchTerm = useDebounce(searchVal, 500)
  useEffect(() => {
    if (debouncedSearchTerm) {
      const newUrl = `/searchAll/${debouncedSearchTerm}`
      if (newUrl !== history.location.pathname) {
        history.push(`/searchAll/${debouncedSearchTerm}`)
      }
    } else {
      if (history.location.pathname.includes('searchAll')) {
        history.push('/')
      }
    }
    setSearchVal(debouncedSearchTerm)
    /* eslint-disable react-hooks/exhaustive-deps*/
  }, [debouncedSearchTerm])

  return (
    <div className="site-wide-search" style={{ margin: '1em 0' }}>
      <Input
        value={searchVal || ''}
        onChange={(e) => setSearchVal(e.target.value)}
        placeholder="Search"
        startAdornment={
          <InputAdornment position="start">
            <Search />
          </InputAdornment>
        }
        fullWidth
      />
      <SearchResults />
    </div>
  )
}

export default SearchAll
