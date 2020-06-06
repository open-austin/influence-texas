import React from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@apollo/react-hooks'
import { gql } from 'apollo-boost'
import PaginatedList, {
  LoadingListItem,
  ShortLoadingListBody,
} from './PaginatedList'
import { format } from 'date-fns'
import SimpleTabs from './SimpleTabs'
import LegislatorsList from './LegislatorList'
import CustomLink from './CustomLink'
import { BillSquare } from '../styles'
import { Typography, Button } from '@material-ui/core'
import OpenInNewIcon from '@material-ui/icons/OpenInNew'
import { getDebugQuery } from '../utils'

const GET_BILL = gql`
  query Bill($id: Int!) {
    bill(pk: $id) {
      chamber
      billId
      title
      billText
      session
      subjects {
        edges {
          node {
            label
          }
        }
      }
      sponsors {
        totalCount
        edges {
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
      actionDates {
        totalCount
        edges {
          node {
            classification
            description
            date
          }
        }
      }
    }
    ${getDebugQuery()}
  }
`

function BillDetailPage() {
  const { id } = useParams()
  const { data, loading, error } = useQuery(GET_BILL, {
    variables: { id },
  })
  document.title = `${data ? data.bill.billId : ''} - Influence Texas`
  if (error) {
    return 'server error'
  }
  const fullBillData = data ? data.bill : {}
  if (!loading) {
    fullBillData.actionDates.edges.reverse()
  }

  return (
    <div>
      <CustomLink to="/bills"> ← All Bills</CustomLink>

      {loading ? (
        LoadingListItem
      ) : (
        <div style={{ display: 'flex', margin: '1em 0' }}>
          <BillSquare billId={fullBillData.billId} />
          <div style={{ margin: '0 1em', flexGrow: 1 }}>
            <Typography variant="h5">{fullBillData.billId}</Typography>
            <div style={{ textTransform: 'capitalize' }}>
              {fullBillData.chamber && fullBillData.chamber.toLowerCase()}
            </div>
            <div>Session {fullBillData.session}</div>
          </div>
          <Button
            variant="outlined"
            color="primary"
            size="small"
            href={fullBillData.billText}
            target="_blank"
            style={{ height: 'fit-content' }}
          >
            <OpenInNewIcon fontSize="small" />{' '}
            <Typography variant="h6">Full Bill Text</Typography>
          </Button>
        </div>
      )}
      <div style={{ margin: '1em 0' }}>{fullBillData.title}</div>
      <div style={{ textTransform: 'capitalize' }}>
        {' '}
        {fullBillData.subjects &&
          fullBillData.subjects.edges.map((d) => {
            const [subject, parens] = d.node.label
              .replace(/--/g, '—')
              .toLowerCase()
              .split('(')
            return (
              <span key={d.node.label}>
                {subject} <span style={{ opacity: 0.5 }}>({parens} </span>
              </span>
            )
          })}
      </div>
      <SimpleTabs
        saveToUrl
        tabs={[
          {
            label: `Actions (${
              loading ? 'loading' : fullBillData.actionDates.totalCount
            })`,
            content: (
              <PaginatedList
                data={fullBillData.actionDates}
                title="Actions"
                className="no-scroll"
                loading={loading}
                columns={[
                  {
                    field: 'node.description',
                    render: (rowData) => (
                      <div style={{ textTransform: 'capitalize' }}>
                        <div
                          style={{
                            textTransform: 'uppercase',
                            opacity: 0.5,
                          }}
                        >
                          {rowData.node.classification.replace(/-/g, ' ')}
                        </div>
                        <div>{rowData.node.description}</div>
                      </div>
                    ),
                  },
                  {
                    field: 'node.date',
                    render: (rowData) => (
                      <div style={{ textAlign: 'right' }}>
                        {format(new Date(rowData.node.date), 'PP')}
                      </div>
                    ),
                  },
                ]}
                loading={loading}
                rowsPerPage={100}
                loadingListBody={ShortLoadingListBody}
              />
            ),
          },
          {
            label: `Sponsors (${
              loading ? 'loading' : fullBillData.sponsors.totalCount
            })`,
            content: (
              <div className="detail-page">
                <LegislatorsList
                  data={fullBillData.sponsors}
                  title="Sponsors"
                  rowsPerPage={100}
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

export default BillDetailPage
