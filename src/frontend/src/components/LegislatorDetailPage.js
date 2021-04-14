import React from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@apollo/react-hooks'
import { gql } from 'apollo-boost'
import {
  Typography,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@material-ui/core'

import OpenInNewIcon from '@material-ui/icons/OpenInNew'
import SimpleTabs from 'components/SimpleTabs'
import PaginatedList, {
  LoadingListItem,
  ShowMoreList,
} from 'components/PaginatedList'
import BillList from 'components/BillList'
import TexasDistrictMap from 'components/TexasDistrictMap'
import CustomLink from 'components/CustomLink'
import { formatMoney, getDebugQuery } from 'utils'
import { ImageSquare } from 'styles'
import FilterSection from './FilterSection'
import styled from 'styled-components'
import {
  CLASSIFICATION_FILTERS,
  MANY_SPONSORS_FILTER,
  PARTY_FILTERS,
} from './BillsPage'
import { MuiThemeProvider } from '@material-ui/core/styles'
import { billTheme } from 'theme'

const GET_LEG = gql`
  query Legislator($id: Int!) {
    legislator(pk: $id) {
      pk
      name
      party
      chamber
      photoUrl
      url
      district
      contributions {
        edges {
          node {
            cycleTotal
            donor {
              pk
              fullName
              city
              state
              employer
              occupation
            }
          }
        }
      }
      billsSponsored {
        totalCount
      }
      financialDisclosures {
        year
        electedOfficer
        jobs {
              heldBy
              position
              employer
        }
        stocks {
              name
              heldBy
              numShares
        }
        boards {
              heldBy
              position
              name
        }
        gifts {
              recipient
              description
              donor
        }
      }
    }
    ${getDebugQuery()}
  }
`

const BILLS_SPONSORED = gql`
  query AllBills(
    $classification: String
    $party: String
    $chamber: String
    $sponsorId: String
    $multipleSponsors: Boolean
    $first: Int
    $last: Int
    $after: String
    $before: String
  ) {
    bills(
      classification: $classification
      chamber: $chamber
      sponsorId: $sponsorId
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

export const BillsWrapper = styled.div`
  button {
    border-bottom: none !important;
  }
`

function HeldByDiv({ heldBy }) {
  return (
    HeldByName[heldBy] && (
      <span style={{ opacity: 0.5 }}> ({HeldByName[heldBy]})</span>
    )
  )
}

const HeldByName = {
  FILER: '',
  SPOUSE: 'Spouse',
  DEPENDENT: 'Dependent',
}

function heldByOrder(a, b) {
  return a.heldBy === 'FILER' ? -1 : 1
}

function FinancialDisclosure({ disclosure, loading }) {
  if (!disclosure) return null
  return (
    <div>
      <ShowMoreList
        title="Employers"
        rows={disclosure.jobs.sort(heldByOrder) || []}
        totalCount={!loading && disclosure.jobs.length}
        render={(rowData) => (
          <LabelDetail
            label={
              <span>
                {rowData.employer} <HeldByDiv {...rowData} />
              </span>
            }
            detail={rowData.position}
          />
        )}
        collapsable
      />
      <div style={{ margin: '3rem' }} />
      <ShowMoreList
        hideIfNoResults
        title="Boards"
        rows={disclosure.boards.sort(heldByOrder) || []}
        totalCount={!loading && disclosure.boards.length}
        render={(rowData) => (
          <LabelDetail
            label={
              <span>
                {rowData.name} <HeldByDiv {...rowData} />
              </span>
            }
            detail={rowData.position}
          />
        )}
        collapsable
      />
      <div style={{ margin: '3rem' }} />
      <ShowMoreList
        hideIfNoResults
        title="Stocks"
        rows={disclosure.stocks.sort(heldByOrder)}
        totalCount={!loading && disclosure.stocks.length}
        render={(rowData) => (
          <LabelDetail
            label={
              <span>
                {rowData.name} <HeldByDiv {...rowData} />
              </span>
            }
            detail={rowData.numShares}
          />
        )}
        collapsable
        defaultOpen={disclosure.stocks.length < 10}
      />
      <div style={{ margin: '3rem' }} />

      <ShowMoreList
        hideIfNoResults
        title="Gifts"
        rows={disclosure.gifts}
        totalCount={!loading && disclosure.gifts.length}
        render={(rowData) => (
          <LabelDetail
            label={
              <span>
                {rowData.donor} <HeldByDiv {...rowData} />
              </span>
            }
            detail={rowData.description}
          />
        )}
      />
    </div>
  )
}

function FinancialDisclosureSection({ disclosures, loading }) {
  const [disclosureIdx, setDisclosureIdx] = React.useState(0)
  if (!disclosures) return null
  if (disclosures.length === 0) return 'No disclosures found.'

  return (
    <div>
      <div style={{ padding: '1em', textAlign: 'center' }}>
        <FormControl>
          <InputLabel id="demo-simple-select-label">Year</InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={disclosureIdx}
            onChange={(e) => setDisclosureIdx(e.target.value)}
          >
            {disclosures.map((d, i) => (
              <MenuItem value={i}> {d.year} </MenuItem>
            ))}
          </Select>
        </FormControl>
      </div>
      <FinancialDisclosure
        disclosure={disclosures[disclosureIdx]}
        loading={loading}
      />
    </div>
  )
}
function LabelDetail({ label, detail }) {
  return (
    <div>
      {label}
      <div style={{ opacity: 0.5 }}>{detail}</div>
    </div>
  )
}

function LegislatorDetailPage() {
  const { id } = useParams()
  const { data, loading, error } = useQuery(GET_LEG, {
    variables: { id },
  })
  document.title = `${data ? data.legislator.name : ''} - Influence Texas`
  if (error) {
    return 'server error'
  }
  const fullLegData = data ? data.legislator : {}
  return (
    <div className="detail-page">
      <CustomLink to="/legislators"> ← All Legislators</CustomLink>
      {loading ? (
        <div>{LoadingListItem}</div>
      ) : (
        <div style={{ display: 'flex', margin: '1em 0' }}>
          <ImageSquare photoUrl={fullLegData.photoUrl} />
          <div style={{ margin: '0 1em', flexGrow: 1 }}>
            <Typography variant="h5">{fullLegData.name}</Typography>
            <div style={{ textTransform: 'capitalize' }}>
              {fullLegData.chamber && fullLegData.chamber.toLowerCase()} (
              {fullLegData.party})
            </div>
            <div>District {fullLegData.district}</div>
          </div>
          <Button
            variant="outlined"
            color="primary"
            size="small"
            href={fullLegData.url}
            target="_blank"
            style={{ height: 'fit-content' }}
          >
            <OpenInNewIcon fontSize="small" />{' '}
            <Typography variant="h6">Full Biography</Typography>
          </Button>
        </div>
      )}

      <SimpleTabs
        saveToUrl
        tabs={[
          {
            label: `Top Donors (${
              loading ? 'loading' : fullLegData.contributions.edges.length
            })`,
            className: 'donor-theme',
            content: (
              <div>
                <PaginatedList
                  url="donors/donor"
                  pk="node.donor.pk"
                  title="Top Donors"
                  data={fullLegData.contributions}
                  totalCount={
                    !loading && fullLegData.contributions.edges.length
                  }
                  columns={[
                    {
                      render: (rowData) => {
                        return (
                          <div>
                            {rowData.node.donor.fullName}
                            <div style={{ opacity: 0.5 }}>
                              {rowData.node.donor.occupation}
                              {rowData.node.donor.occupation &&
                                rowData.node.donor.employer &&
                                ' ・ '}
                              {rowData.node.donor.employer}
                            </div>
                          </div>
                        )
                      },
                    },
                    {
                      render: (rowData) => {
                        return (
                          <div style={{ textAlign: 'right' }}>
                            {formatMoney(rowData.node.cycleTotal)}
                            <div style={{ opacity: 0.5 }}>
                              {rowData.node.donor.city},{' '}
                              {rowData.node.donor.state}
                            </div>
                          </div>
                        )
                      },
                    },
                  ]}
                  loading={loading}
                  rowsPerPage={100}
                />
              </div>
            ),
          },
          {
            label: `Financial Disclosures (${
              loading ? 'loading' : fullLegData.financialDisclosures?.length
            })`,
            content: (
              <FinancialDisclosureSection
                disclosures={fullLegData.financialDisclosures}
                loading={loading}
              />
            ),
          },
          {
            label: `Bills Sponsored (${
              loading ? 'loading' : fullLegData.billsSponsored.totalCount
            })`,
            className: 'bill-theme',
            content: (
              <MuiThemeProvider theme={billTheme}>
                <BillsWrapper>
                  <BillList
                    gqlQuery={BILLS_SPONSORED}
                    gqlVariables={{ sponsorId: id }}
                    rowsPerPage={100}
                    title={
                      <>
                        <FilterSection
                          hr={false}
                          style={{ width: '100%' }}
                          title={
                            <Typography variant="h6">
                              Bills Sponsored
                            </Typography>
                          }
                          tags={{
                            party: PARTY_FILTERS,
                            multipleSponsors: MANY_SPONSORS_FILTER,
                            classification: CLASSIFICATION_FILTERS,
                          }}
                        />
                      </>
                    }
                  />
                </BillsWrapper>
              </MuiThemeProvider>
            ),
          },
          {
            label: 'District Map',
            content: (
              <div>
                <TexasDistrictMap
                  chamber={fullLegData.chamber}
                  district={fullLegData.district}
                  loading={loading}
                />
              </div>
            ),
          },
        ]}
      />
    </div>
  )
}

export default LegislatorDetailPage
