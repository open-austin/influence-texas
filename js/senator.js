"use strict";

//var followTheMoneyURL = "https://api2.followthemoney.org/";
//var followTheMoneyAPIKey = "c6c2821ad92eb7b9da254be62f039f33"; // djwehrle
var followTheMoneyAPIKey = "b826388da09fa13dc0f94988d0d82e6d"; // d861073@mvrht.net
//https://api2.followthemoney.org/?&APIKey=c6c2821ad92eb7b9da254be62f039f33&mode=json

var hb100Tags = "Automotive;";
var sb1004Tags = "Telecom Services &amp; Equipment; Telephone Utilities;";

$(document).ready(function() {
   
    var url = window.location.href;
    var districtNo = url.substring(url.search("district-no=") + "district-no=".length);
    
    GetData(districtNo);
    
    $("#votes tbody tr").click(function() {
        FilterContributors($(".tags", this).html());
        $(this).addClass("bg-primary");
    });
    
    $("#clearFilters").click(function () {
        
        // Clear custom filters
        $.fn.dataTable.ext.search = [];
        
        // Clear Contributors filter
        $("#contributors").DataTable().search("").draw();
        
        // Clear Votes filter
        $("#votes").DataTable().search("").draw();
        
        // Clear highlighted rows
        $(".bg-primary").removeClass("bg-primary");
        
    });
    
});

function FilterContributors(industries) {
    
    console.log("Filtering Contributors.");
    
    // Reset filters first
    $("#clearFilters").click();
    
    $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
                                   
        // These rules apply to every DataTable so need to filter to specific table in the rule itself
        if (settings.nTable.id === "contributors") {
            
            // Remove special characters from search
            var contributorsFilter = industries.replace(/[&][^;]*[;]/g, "");
            
            // Check if Contributing Industy exists in tags from Votes table
            // Remove special characters first
            var dataToSearch = data[0].replace(/[&]/g, "");
            
            return contributorsFilter.search(dataToSearch) >= 0;
            
        }
        
        return true;
    });
    
    $("#contributors").DataTable().draw();
    
}

function FilterVotes(tags) {
    
    console.log("Filtering Votes.");
    
    // Reset filters first
    $("#clearFilters").click();
    
    // Remove special characters from search
    var votesFilter = tags.replace(/[&][^;]*[;]/g, "");
    
    $("#votes").DataTable().search(votesFilter).draw();
}

function GetData(districtNo) {
    
    $.ajax({
        url: "data/senators.json",
        dataType: "json",
        success: function(data) {
            console.log("Retrieved Senators.");
            
            var senator = {};
            
            $.each(data, function() {
                if (this.DistrictNo == districtNo) {
                    console.log("Senator found!");
                    senator = this;
                }
            });
            
            PopulatePage(senator);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("Error retrieving Senator.");
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        }
    });
    
}

function PopulatePage(senator) {
    
    // Set Senator Name
    var senatorName = "Senator " + senator.FirstName + " " + senator.LastName + " (" + senator.Party + ")";
    document.title = senatorName + " - Accountability Texas";
    $("#senatorName").text(senatorName);
    
    // Set District Number
    $("#district").text("District " + senator.DistrictNo  + " - " + senator.Town);
    
    // Set image
    $("#senatorImg").prop("src", "images/senators/" + senator.DistrictNo + "-headshot.jpg");
    
    PopulateContributors(senator);
    PopulateVotes(senator);
    
}

function PopulateContributors(senator) {
    
    // 1) Find Filer ID for Senator
    var state = "TX";
    var year = "2016";
    var industries = "24,25,109";
    /*
    var filerURL = "https://api2.followthemoney.org/?"
        + "s=" + state
        + "&y=" + year
        + "&d-cci=" + industries
        + "&gro=f-eid,d-cci" // group by Filer
        + "&APIKey=" + followTheMoneyAPIKey
        + "&mode=json";
    */
    var filerURL = "data/filers.json";
    
    console.log("Filer URL: " + filerURL);
    
    $.ajax({
        url: filerURL,
        method: "GET",
        dataType: "json",
        success: function(data) {
            console.log("Retrieved Filers.");
            
            // Find Filer based on Filer (name)            
            // Filer names might not exactly match; find first and last name
            var filerID;
            
            $.each(data.records, function() {
                var filerName = this.Filer.Filer;
                if (filerName.search(senator.FirstName.toUpperCase()) !== -1 &&
                   filerName.search(senator.LastName.toUpperCase()) !== -1) {
                    
                    filerID = this.Filer.id;
                    console.log("Found Filer ID: " + filerID);
                    
                    return false;
                    
                }
            });
            
            // 2) Find Contributors for Senator using Filer ID
            /*
            var contributorsURL = "https://api2.followthemoney.org/?"
                + "s=" + state 
                + "&y=" + year
                + "&f-eid=" + filerID
                + "&gro=f-eid,d-cci" // group by Filer, General Industry
                + "&APIKey=" + followTheMoneyAPIKey
                + "&mode=json";
            */
            
            var contributorsURL = "data/contributors_0.json";
            
            console.log("Contributors URL: " + contributorsURL);
            
            $.ajax({
                url: contributorsURL,
                type: "GET",
                success: function(data) {
                    
                    console.log("Retrieved Contributors page 1.");
                    
                    var records = [];
                    
                    $.each(data.records, function() {
                        if (this.Filer.id === filerID) {
                            records.push(this);
                        }
                    });
                    
                    var moreAJAXCalls = [];
                    
                    // Check if more pages need to be downloaded
                    for (var i = data.metaInfo.paging.currentPage + 1; i <= data.metaInfo.paging.maxPage; i++) {
                        
                        console.log("Retrieving Contributors page " + i + " of " + data.metaInfo.paging.maxPage + ".");
                                                
                        //var moreContributorsURL = contributorsURL + "&p=" + i; // Production
                        var moreContributorsURL = "data/contributors_" + i + ".json";
                        console.log("More Contributors URL: " + moreContributorsURL);
                        
                        var moreAJAX = $.ajax({
                            url: moreContributorsURL,
                            type: "GET",
                            success: function(moreData) {
                                
                                $.each(moreData.records, function() {
                                    if (this.Filer.id === filerID) {
                                        records.push(this);
                                    }
                                });
                                
                                console.log("Retrieved Contributors page " + moreData.metaInfo.paging.currentPage + ".");
                                
                            }
                        });
                        
                        moreAJAXCalls.push(moreAJAX);
                        
                    }
                    
                    // Need to wait for AJAX calls to finish
                    $.when.apply($, moreAJAXCalls).done(function() {
                        
                        console.log("All Contributors retrieved.");
                        
                        // 3) Fill Contributors DataTable
                        $("#contributors").DataTable({
                            dom: "", // Hide search bar
                            filter: true,
                            info: false,
                            paging: false,
                            data: records,
                            columns: [
                                { data: "General_Industry.General_Industry" },
                                { data: function(row, type, val, meta) {
                                    return "$" + parseInt(row.Total_$.Total_$).toLocaleString();
                                }}
                            ],
                            order: [[1, "desc"]] // Order by largest amounts
                        });
                        
                        $("#contributors tbody tr").click(function() {
                            FilterVotes($("td", this).html());
                            $(this).addClass("bg-primary");
                        });
                        
                    });
                    
                }
            });
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("Error retrieving Filers.");
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        }
    });
    
}

function PopulateVotes(senator) {
    
    // Fill Votes DataTable
    $("#hb100Tags").html(hb100Tags);
    $("#sb1004Tags").html(sb1004Tags);
    
    $("#hb100Vote").html(senator.HB100Vote);
    $("#sb1004Vote").html(senator.SB1004Vote);
    
    $("#votes").DataTable({
        dom: "",
        filter: true,
        info: false,
        paging: false
    });
    
}