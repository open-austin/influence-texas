import React from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@apollo/react-hooks'
import { gql } from 'apollo-boost'
import { Typography, Button } from '@material-ui/core'

import OpenInNewIcon from '@material-ui/icons/OpenInNew'
import SimpleTabs from 'components/SimpleTabs'
import PaginatedList, {
  LoadingListItem,
  SimpleList,
} from 'components/PaginatedList'
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

function FinancialDisclosure({ disclosure, loading }) {
  if (!disclosure) return null
  debugger
  return (
    <div>
      <div style={{ margin: '1rem', opacity: 0.8 }}>{disclosure.year}</div>
      {/* <PaginatedList
        className="no-scroll"
        collapsable
        hideIfNoResults
        title="Employers"
        data={disclosure.jobs || []}
        totalCount={!loading && disclosure.jobs.length}
        columns={[
          { render: (rowData) => rowData.employer },
          { render: (rowData) => rowData.position },
          { render: (rowData) => rowData.heldBy },
        ]}
      /> */}
      {/* <div style={{ margin: '3rem' }} />
      <PaginatedList
        collapsable
        hideIfNoResults
        title="Boards"
        data={disclosure?.boards}
        totalCount={!loading && disclosure?.boards.length}
        columns={[
          { render: (rowData) => rowData.name },
          { render: (rowData) => rowData.position },
          { render: (rowData) => rowData.heldBy },
        ]}
      />
      <div style={{ margin: '3rem' }} />
      <PaginatedList
        collapsable
        hideIfNoResults
        title="Stocks"
        data={disclosure?.stocks}
        totalCount={!loading && disclosure?.stocks.length}
        columns={[
          { render: (rowData) => rowData.name },
          { render: (rowData) => rowData.numShares },
          { render: (rowData) => rowData.heldBy },
        ]}
      />
      <div style={{ margin: '3rem' }} />

      <PaginatedList
        collapsable
        hideIfNoResults
        title="Gifts"
        data={disclosure?.gifts}
        totalCount={!loading && disclosure?.gifts.length}
        columns={[
          { render: (rowData) => rowData.description },
          { render: (rowData) => rowData.donor },
          { render: (rowData) => rowData.recipient },
        ]}
      /> */}
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
            label: `Financial Disclosures (${fullLegData.financialDisclosures?.length})`,
            content: (
              <div>
                <SimpleList
                  title="Employers"
                  rows={fullLegData.financialDisclosures?.[0]?.jobs || []}
                  totalCount={
                    !loading &&
                    fullLegData.financialDisclosures?.[0]?.jobs.length
                  }
                  columns={[
                    { render: (rowData) => rowData.employer },
                    { render: (rowData) => rowData.position },
                    { render: (rowData) => rowData.heldBy },
                  ]}
                />
                <div style={{ margin: '3rem' }} />
                <SimpleList
                  hideIfNoResults
                  title="Boards"
                  rows={fullLegData.financialDisclosures?.[0]?.boards || []}
                  totalCount={
                    !loading &&
                    fullLegData.financialDisclosures?.[0]?.boards.length
                  }
                  columns={[
                    { render: (rowData) => rowData.name },
                    { render: (rowData) => rowData.position },
                    { render: (rowData) => rowData.heldBy },
                  ]}
                />
                <div style={{ margin: '3rem' }} />
                <SimpleList
                  hideIfNoResults
                  title="Stocks"
                  rows={fullLegData.financialDisclosures?.[0]?.stocks}
                  totalCount={
                    !loading &&
                    fullLegData.financialDisclosures?.[0]?.stocks.length
                  }
                  columns={[
                    { render: (rowData) => rowData.name },
                    { render: (rowData) => rowData.numShares },
                    { render: (rowData) => rowData.heldBy },
                  ]}
                />
                <div style={{ margin: '3rem' }} />

                <SimpleList
                  hideIfNoResults
                  title="Gifts"
                  rows={fullLegData.financialDisclosures?.[0]?.gifts}
                  totalCount={
                    !loading &&
                    fullLegData.financialDisclosures?.[0]?.gifts.length
                  }
                  columns={[
                    { render: (rowData) => rowData.description },
                    { render: (rowData) => rowData.donor },
                    { render: (rowData) => rowData.recipient },
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
