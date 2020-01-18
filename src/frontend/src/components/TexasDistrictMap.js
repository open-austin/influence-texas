import React, { useState } from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
  ZoomableGroup
} from "react-simple-maps";
import Texas_State_Senate_Districts from "../data/Texas_State_Senate_Districts_Simplified";
import Texas_State_House_Districts from "../data/Texas_State_House_Districts_Simplified";
import ReactTooltip from "react-tooltip";
import { gql } from "apollo-boost";
import { useQuery } from "@apollo/react-hooks";
import { useHistory } from "react-router-dom";
import { capitalize } from "../utils";
import { legTheme } from "../theme";

const ALL_LEG = gql`
  {
    legislators {
      edges {
        node {
          district
          pk
          chamber
          name
        }
      }
    }
  }
`;

export default function TexasDistrictMap({ district, chamber = "HOUSE" }) {
  const [tooltipContent, setTooltipContent] = useState("");
  const { data } = useQuery(ALL_LEG);
  const history = useHistory();
  const legData = data
    ? data.legislators.edges.reduce(
        (acc, d) => {
          acc[d.node.chamber].push(d.node);
          return acc;
        },
        { HOUSE: [], SENATE: [] }
      )
    : { HOUSE: [], SENATE: [] };
  legData.HOUSE.sort((l1, l2) => l1.district - l2.district);
  legData.SENATE.sort((l1, l2) => l1.district - l2.district);
  const geography =
    chamber === "HOUSE"
      ? Texas_State_House_Districts
      : Texas_State_Senate_Districts;
  return (
    <>
      <ReactTooltip>{tooltipContent}</ReactTooltip>
      <ComposableMap
        data-tip=""
        width={400}
        height={350}
        projection="geoAlbersUsa"
      >
        <ZoomableGroup zoom={1.5} center={[-100, 31]}>
          <Geographies geography={geography}>
            {arg => {
              return arg.geographies.map((geo, i) => {
                const leg = legData[chamber][i] || {};

                return (
                  <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    onMouseEnter={() => {
                      setTooltipContent(
                        `${capitalize(chamber)} District ${leg.district} ${
                          leg.name
                        }`
                      );
                    }}
                    onMouseLeave={() => {
                      setTooltipContent("");
                    }}
                    onClick={() => {
                      history.push(`/legislators/legislator/${leg.pk}`);
                    }}
                    style={{
                      default: {
                        fill: district
                          ? leg.district === district
                            ? legTheme.palette.primary.main
                            : "white"
                          : "#D6D6DA",
                        stroke:
                          district && leg.district === district
                            ? legTheme.palette.primary.main
                            : "#EAEAEC"
                      },
                      hover: {
                        fill: legTheme.palette.primary.main,
                        outline: "none"
                      },
                      pressed: {
                        fill: legTheme.palette.primary.main,
                        outline: "none"
                      }
                    }}
                  />
                );
              });
            }}
          </Geographies>
        </ZoomableGroup>
      </ComposableMap>
    </>
  );
}
