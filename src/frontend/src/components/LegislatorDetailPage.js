import React from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@apollo/react-hooks'
import { gql } from 'apollo-boost'
import { Typography, Button } from '@material-ui/core'

import OpenInNewIcon from '@material-ui/icons/OpenInNew'
import SimpleTabs from 'components/SimpleTabs'
import PaginatedList, { LoadingListItem } from 'components/PaginatedList'
import BillList from 'components/BillList'
import TexasDistrictMap from 'components/TexasDistrictMap'
import CustomLink from 'components/CustomLink'
import { formatMoney, getDebugQuery } from 'utils'
import { ImageSquare } from 'styles'

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
        edges {
          node {
            pk
            billId
            title
          }
        }
      }
      financialDisclosures {
        totalCount
        edges {
          node {
            year
            electedOfficer
            jobs {
              edges {
                node {
                  heldBy
                  position
                  employer
                }
              }
            }
            stocks {
              edges {
                node {
                  name
                  heldBy
                  numShares
                }
              }
            }
            boards {
              edges {
                node {
                  heldBy
                  position
                  name
                }
              }
            }
            gifts {
              edges {
                node {
                  recipient
                  description
                  donor
                }
              }
            }
          }
        }
      }
    }
    ${getDebugQuery()}
  }
`

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
            label: `Financial Disclosures (${fullLegData.financialDisclosures?.edges.length})`,
            content: (
              <div>
                <PaginatedList
                  title="Employers"
                  data={fullLegData.financialDisclosures?.edges[0]?.node.jobs}
                  totalCount={
                    !loading &&
                    fullLegData.financialDisclosures?.edges[0]?.node.jobs.edges
                      .length
                  }
                  columns={[
                    { render: (rowData) => rowData.node.employer },
                    { render: (rowData) => rowData.node.position },
                    { render: (rowData) => rowData.node.heldBy },
                  ]}
                />
                <div style={{ margin: '3rem' }} />
                <PaginatedList
                  hideIfNoResults
                  title="Boards"
                  data={fullLegData.financialDisclosures?.edges[0]?.node.boards}
                  totalCount={
                    !loading &&
                    fullLegData.financialDisclosures?.edges[0]?.node.boards
                      .edges.length
                  }
                  columns={[
                    { render: (rowData) => rowData.node.name },
                    { render: (rowData) => rowData.node.position },
                    { render: (rowData) => rowData.node.heldBy },
                  ]}
                />
                <div style={{ margin: '3rem' }} />
                <PaginatedList
                  hideIfNoResults
                  title="Stocks"
                  data={fullLegData.financialDisclosures?.edges[0]?.node.stocks}
                  totalCount={
                    !loading &&
                    fullLegData.financialDisclosures?.edges[0]?.node.stocks
                      .edges.length
                  }
                  columns={[
                    { render: (rowData) => rowData.node.name },
                    { render: (rowData) => rowData.node.numShares },
                    { render: (rowData) => rowData.node.heldBy },
                  ]}
                />
                <div style={{ margin: '3rem' }} />

                <PaginatedList
                  hideIfNoResults
                  title="Gifts"
                  data={fullLegData.financialDisclosures?.edges[0]?.node.gifts}
                  totalCount={
                    !loading &&
                    fullLegData.financialDisclosures?.edges[0]?.node.gifts.edges
                      .length
                  }
                  columns={[
                    { render: (rowData) => rowData.node.description },
                    { render: (rowData) => rowData.node.donor },
                    { render: (rowData) => rowData.node.recipient },
                  ]}
                />
              </div>
            ),
          },
          {
            label: `Bills Sponsored (${
              loading ? 'loading' : fullLegData.billsSponsored.totalCount
            })`,
            content: (
              <div>
                <BillList
                  title="Bills Sponsored"
                  data={fullLegData.billsSponsored}
                  rowsPerPage={100}
                  loading={loading}
                />
              </div>
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
