import React from 'react'
import { Link, Typography } from '@material-ui/core'

export default function About() {
  return (
    <div style={{ marginTop: '1rem' }}>
      <Typography variant="h6">About</Typography>
      <div class="container">
        <h4>Get Involved</h4>
        <p>
          Are you passionate about government transparency? Please sign up for
          our mailing list to stay up to date on our progress and give us
          feedback on features you would like to see.
          <Link
            href="https://www.influencetexas.com/sign-up/"
            target="_blank"
            rel="noopener noreferrer"
          >
            {' '}
            Sign up here!
          </Link>
        </p>
        <p>
          This nonpartisan open-source project creates access to campaign
          finance information and bill information for Texas state politicians
          from the most recent (86th) legislative session. The project began at{' '}
          <Link
            href="http://atxhackforchange.org/"
            target="_blank"
            rel="noopener noreferrer"
          >
            ATX Hack for Change
          </Link>{' '}
          in 2017, and is supported by{' '}
          <Link
            href="https://www.open-austin.org/"
            target="_blank"
            rel="noopener noreferrer"
          >
            Open Austin
          </Link>{' '}
          and{' '}
          <Link
            href="https://influencetexas.com"
            target="_blank"
            rel="noopener noreferrer"
          >
            Influence Texas P.B.C.
          </Link>
        </p>
        <h4>About Our Data</h4>
        <p>
          Lawmakers’ <b>Personal Financial Statement</b> records were obtained{' '}
          byInfluence Texas via an open records request to the Texas{' '}
          EthicsCommission. Lawmakers and state officials are required to{' '}
          disclose business entities that have ownership in, as well as stocks{' '}
          and other financial interests. The state’s annual filing deadline is{' '}
          April. Thus, the data in the current Influence Texas app represents
          the January 2019 throughDecember 2019 calendar year. The date for the
          2020 calendar year will not be available until April 2021.
        </p>
        <p>
          <b>Legislature, Bill, and Voting</b> records are provided by{' '}
          <Link
            href="https://openstates.org/"
            target="_blank"
            rel="noopener noreferrer"
          >
            Open States
          </Link>
          , a project supported by the nonprofit{' '}
          <Link
            href="http://openmediafoundation.org/"
            target="_blank"
            rel="noopener noreferrer"
          >
            Open Media Foundation
          </Link>{' '}
          that scrapes data from the Texas House and Senate journals. This app
          features records from the most recent legislative session.
        </p>
        <p>
          <b>Campaign finance</b> records are supplied by the nonprofit{' '}
          <Link
            href="http://www.tpj.org/"
            target="_blank"
            rel="noopener noreferrer"
          >
            Texans for Public Justice
          </Link>
          , which obtains <i>Contribution and Expenditure</i> data dutifully
          filed with the Texas Ethics Commission by all candidates, political
          committees, and political parties from the campaign cycle just prior
          to the current legislative session. This app shows the top 25 donors
          to each politician and the top 25 donations of each featured donor
          that has contributed an aggregate amount of $1,000 or more.
        </p>
        <p>
          THE DATA IS PROVIDED “ASIS” AND INFLUENCE TEXAS,ITS AFFILIATES AND
          THEIR RESPECTIVE THIRD PARTY SUPPLIERS HEREBY EXPRESSLY DISCLAIM ANY
          AND ALL REPRESENTATIONS AND WARRANTIES OF EVERY KIND, EXPRESS AND/OR
          IMPLIED,INCLUDING WITHOUT LIMITATION ANY WARRANTIES OF
          MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR USE,TITLE OR
          NON-INFRINGEMENT, AS TO THE DATA, INCLUDING THE INFORMATION, CONTENT,
          DATA, DERIVED DATA OR PRODUCTS CONTAINED THERE IN OR THE RESULTS
          OBTAINED OR DERIVED THERE FROM BY THEIR USE, AND AS TO THE PERFORMANCE
          THEREOF. NEITHER THE DATA, ITS AFFILIATES NOR THEIR RESPECTIVE THIRD
          PARTY SUPPLIERS GUARANTEE THE ADEQUACY, ACCURACY, TIMELINESS OR
          COMPLETENESS OF THE DATA OR ANY COMPONENT THEREOF. THE DATA, ITS
          AFFILIATES AND THEIR RESPECTIVE THIRD PARTY SUPPLIERS SHALL NOT BE
          SUBJECT TO ANY DAMAGES OR LIABILITY FOR ANY ERRORS, OMISSIONS,
          INTERRUPTIONS, MALFUNCTIONS OR DELAYS IN THE DATA. FURTHER, THE DATA,
          ITS AFFILIATES AND THEIR RESPECTIVE THIRD PARTY SUPPLIERS SHALL NOT BE
          LIABLE FOR ANY CLAIMS AGAINST LICENSEE BY THIRD PARTIES.
        </p>
        <h4>TOS and Privacy</h4>
        Please read our{' '}
        <Link
          href="https://influencetexas.com/os-tos"
          target="_blank"
          rel="noopener noreferrer"
        >
          TOS
        </Link>{' '}
        and{' '}
        <Link
          href="https://influencetexas.com/os-privacy"
          target="_blank"
          rel="noopener noreferrer"
        >
          Privacy Policy
        </Link>
        .
        <br />
        <br />
        <br />
      </div>
    </div>
  )
}
