"use strict";

$(document).ready(function() {
   
    $("#senators").DataTable({
        ajax: {
            url: "data/senators.json",
            dataSrc: ""
        },
        columns: [
            { data: "DistrictNo" },
            { data: function(row, type, val, meta) {
                return row.FirstName + " " + row.LastName;
            }},
            { data: "Party" }
        ]
    });
    
    // This waits for data to load to attach click event to rows
    $("#senators").on("init.dt", function() {
        $("#senators tbody tr").click(function() {
            window.location.href = "senator.html?district-no=" + $(this).children("td").first().html();
        });
    });
    
    $("#senators").on("page.dt", function() {
        $("#senators tbody tr").click(function() {
            window.location.href = "senator.html?district-no=" + $(this).children("td").first().html();
        });
    });
    
    $("#senators_paginate").click(function() {
        $("#senators tbody tr").click(function() {
            window.location.href = "senator.html?district-no=" + $(this).children("td").first().html();
        });
    });
    
});