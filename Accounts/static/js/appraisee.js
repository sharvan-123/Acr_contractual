    $(window).on('load', function() {
        var url = $("#taggingForm").attr("data-branches-url");
        $.ajax({
            url: url,
            data: {'region': 'region'},
            success: function (data) {
                $("#inputRegion").html(data);
                $('#inputRegion').prop('selectedIndex', $('#inputRegion option[value=" ' +$('#objectInputRegion').text()+ ' "]').index());
                if ($('#objectInputRegion').text()){
                  $.ajax({
                    url: url,
                    data: {'circle': $('#objectInputRegion').text()},
                    success: function (data) {
                        $("#inputRegionVal").val($("#inputRegion option:selected" ).text());
                        $("#inputCircle").html(data);
                        if($('#inputCircle').children('option').length > 4){
                            $("#inputCircle").removeAttr('disabled', 'disabled');
                            $('#inputCircle').prop('selectedIndex', $('#inputCircle option[value=" ' +$('#objectInputCircle').text()+ ' "]').index());
                            if ($('#objectInputCircle').text()){
                              $.ajax({
                                url: url,
                                data: {'division': $('#objectInputCircle').text()},
                                success: function (data) {
                                    $("#inputCircleVal").val($("#inputCircle option:selected" ).text());
                                    $("#inputDivision").html(data);
                                    if($('#inputDivision').children('option').length > 4){
                                        $("#inputDivision").removeAttr('disabled', 'disabled');
                                        $('#inputDivision').prop('selectedIndex', $('#inputDivision option[value=" ' +$('#objectInputDivision').text()+ ' "]').index());
                                        if ($('#objectInputDivision').text()){
                                          $.ajax({
                                            url: url,
                                            data: {'subDivision': $('#objectInputDivision').text()},
                                            success: function (data) {
                                                $("#inputDivisionVal").val($("#inputDivision option:selected" ).text());
                                                $("#inputSubDivision").html(data);
                                                if($('#inputSubDivision').children('option').length > 1){
                                                    $("#inputSubDivision").removeAttr('disabled', 'disabled');
                                                    $('#inputSubDivision').prop('selectedIndex', $('#inputSubDivision option[value=" ' +$('#objectInputSubDivision').text()+ ' "]').index());
                                                    if ($('#objectInputSubDivision').text()){
                                                      $.ajax({
                                                        url: url,
                                                        data: {'dc': $('#objectInputSubDivision').text()},
                                                        success: function (data) {
                                                            $("#inputSubDivisionVal").val($("#inputSubDivision option:selected" ).text());
                                                            $("#inputDC").html(data);
                                                            if($('#inputDC').children('option').length > 1){
                                                                $("#inputDC").removeAttr('disabled', 'disabled');
                                                                $('#inputDC').prop('selectedIndex', $('#inputDC option[value=" ' +$('#objectInputDc').text()+ ' "]').index());
                                                            }
                                                            else{
                                                                $("#inputSubDivision").attr('disabled', 'disabled');
                                                                $("#inputDC").attr('disabled', 'disabled');
                                                            }
                                                        }
                                                      });
                                                    }
                                                }
                                                else{
                                                    $("#inputSubDivision").attr('disabled', 'disabled');
                                                    $("#inputDC").attr('disabled', 'disabled');
                                                }
                                                $("#inputDC").html('<option value="" selected>Select DC...</option>');
                                            }
                                          });
                                        }
                                    }
                                    else{
                                        $("#inputDivision").attr('disabled', 'disabled');
                                        $("#inputSubDivision").attr('disabled', 'disabled');
                                        $("#inputDC").attr('disabled', 'disabled');
                                    }
                                    $("#inputSubDivision").html('<option value="" selected>Select SubDivision...</option>');
                                    $("#inputDC").html('<option value="" selected>Select DC...</option>');
                                }
                              });
                            }
                        }
                        else{
                            $("#inputCircle").attr('disabled', 'disabled');
                            $("#inputDivision").attr('disabled', 'disabled');
                            $("#inputSubDivision").attr('disabled', 'disabled');
                            $("#inputDC").attr('disabled', 'disabled');
                        }
                        $("#inputDivision").html('<option value="" selected>Select Division...</option>');
                        $("#inputSubDivision").html('<option value="" selected>Select SubDivision...</option>');
                        $("#inputDC").html('<option value="" selected>Select DC...</option>');
                    }
                  });
                }
            }
        });
        $.ajax({
            url: url,
            data: {'reportingDesignation': 'reportingDesignation'},
            success: function (data) {
                $("#inputReportingDesignation").html(data);
                $('#inputReportingDesignation').prop('selectedIndex', $('#inputReportingDesignation option[value=" ' +$('#objectInputReportingDesignation').text()+ '"]').index());
                //$("#inputReportingDesignation").removeAttr('disabled', 'disabled');
                $("#inputReportingDesignation").attr('required', true);
                if ($('#objectInputReportingDesignation').text()){
                  $.ajax({
                    url: url,
                    data: {'reportingOfficer': $('#objectInputReportingDesignation').text()},
                    success: function (data) {
                        $("#inputReportingOfficer").html(data);
                        if($('#inputReportingOfficer').children('option').length > 1){
                            $('#inputReportingOfficer').prop('selectedIndex', $('#inputReportingOfficer option[value=" ' +$('#objectInputReportingOfficer').text()+ '"]').index());
                            $("#inputReportingOfficer").removeAttr('disabled', 'disabled');
                            $("#inputReportingOfficer").attr('required', true);
                        }
                        else{
                            $("#inputReportingOfficer").attr('disabled', 'disabled');
                            $("#inputReportingOfficer").removeAttr('required', 'required');
                        }
                    }
                  });
                }
            }
        });
        $.ajax({
            url: url,
            data: {'functionDesignation': 'functionDesignation'},
            success: function (data) {
                console.log(data);
                $("#inputDesignation").html(data);
                $('#inputDesignation').prop('selectedIndex', $('#inputDesignation option[value="' +$('#objectInputDesignation').text()+ '"]').index());
                //$("#inputDesignation").removeAttr('disabled', 'disabled');
                $("#inputDesignation").attr('required', true);
            }
        });
        $.ajax({
            url: url,
            data: {'function': 'function'},
            success: function (data) {
                $("#inputFunction").html(data);
                $('#inputFunction').prop('selectedIndex', $('#inputFunction option[value="' +$('#objectInputFunction').text()+ '"]').index());
                //$("#inputFunction").removeAttr('disabled', 'disabled');
                $("#inputFunction").attr('required', true);
            }
        });
        if($("#isAnotherAppraise").prop('checked')){
            $("#taggingPart2").css('display', 'table');
            $("#addAnotherAppraiseeDiv").css('display', 'none');
            $("#delAnotherTaggingDiv").css('display', 'block');
            $("#inputFromDate2").attr('required', true);
            $("#inputToDate2").attr('required', true);
            $("#inputRegion2").attr('required', true);
            $("#inputReportingDesignation2").attr('required', true);
            $("#inputFunction2").attr('required', true);
            $("#input2").attr('required', true);

            $.ajax({
                url: url,
                data: {'region': 'region'},
                success: function (data) {
                    $("#inputRegion2").html(data);
                    $('#inputRegion2').prop('selectedIndex', $('#inputRegion2 option[value=" ' +$('#objectInputRegion2').text()+ ' "]').index());
                    if ($('#objectInputRegion2').text()){
                      $.ajax({
                        url: url,
                        data: {'circle': $('#objectInputRegion2').text()},
                        success: function (data) {
                            $("#inputRegionVal2").val($("#inputRegion2 option:selected" ).text());
                            $("#inputCircle2").html(data);
                            if($('#inputCircle2').children('option').length > 4){
                                $("#inputCircle2").removeAttr('disabled', 'disabled');
                                $('#inputCircle2').prop('selectedIndex', $('#inputCircle2 option[value=" ' +$('#objectInputCircle2').text()+ ' "]').index());
                                if ($('#objectInputCircle2').text()){
                                  $.ajax({
                                    url: url,
                                    data: {'division': $('#objectInputCircle2').text()},
                                    success: function (data) {
                                        $("#inputCircleVal2").val($("#inputCircle2 option:selected" ).text());
                                        $("#inputDivision2").html(data);
                                        if($('#inputDivision2').children('option').length > 4){
                                            $("#inputDivision2").removeAttr('disabled', 'disabled');
                                            $('#inputDivision2').prop('selectedIndex', $('#inputDivision2 option[value=" ' +$('#objectInputDivision2').text()+ ' "]').index());
                                            if ($('#objectInputDivision2').text()){
                                              $.ajax({
                                                url: url,
                                                data: {'subDivision': $('#objectInputDivision2').text()},
                                                success: function (data) {
                                                    $("#inputDivisionVal2").val($("#inputDivision2 option:selected" ).text());
                                                    $("#inputSubDivision2").html(data);
                                                    if($('#inputSubDivision2').children('option').length > 1){
                                                        $("#inputSubDivision2").removeAttr('disabled', 'disabled');
                                                        $('#inputSubDivision2').prop('selectedIndex', $('#inputSubDivision2 option[value=" ' +$('#objectInputSubDivision2').text()+ ' "]').index());
                                                        if ($('#objectInputSubDivision2').text()){
                                                          $.ajax({
                                                            url: url,
                                                            data: {'dc': $('#objectInputSubDivision2').text()},
                                                            success: function (data) {
                                                                $("#inputSubDivisionVal2").val($("#inputSubDivision2 option:selected" ).text());
                                                                $("#inputDC2").html(data);
                                                                if($('#inputDC2').children('option').length > 1){
                                                                    $("#inputDC2").removeAttr('disabled', 'disabled');
                                                                    $('#inputDC2').prop('selectedIndex', $('#inputDC2 option[value=" ' +$('#objectInputDc2').text()+ ' "]').index());
                                                                }
                                                                else{
                                                                    $("#inputSubDivision2").attr('disabled', 'disabled');
                                                                    $("#inputDC2").attr('disabled', 'disabled');
                                                                }
                                                            }
                                                          });
                                                        }
                                                    }
                                                    else{
                                                        $("#inputSubDivision2").attr('disabled', 'disabled');
                                                        $("#inputDC2").attr('disabled', 'disabled');
                                                    }
                                                    $("#inputDC2").html('<option value="" selected>Select DC...</option>');
                                                }
                                              });
                                            }
                                        }
                                        else{
                                            $("#inputDivision2").attr('disabled', 'disabled');
                                            $("#inputSubDivision2").attr('disabled', 'disabled');
                                            $("#inputDC2").attr('disabled', 'disabled');
                                        }
                                        $("#inputSubDivision2").html('<option value="" selected>Select SubDivision...</option>');
                                        $("#inputDC2").html('<option value="" selected>Select DC...</option>');
                                    }
                                  });
                                }
                            }
                            else{
                                $("#inputCircle2").attr('disabled', 'disabled');
                                $("#inputDivision2").attr('disabled', 'disabled');
                                $("#inputSubDivision2").attr('disabled', 'disabled');
                                $("#inputDC2").attr('disabled', 'disabled');
                            }
                            $("#inputDivision2").html('<option value="" selected>Select Division...</option>');
                            $("#inputSubDivision2").html('<option value="" selected>Select SubDivision...</option>');
                            $("#inputDC2").html('<option value="" selected>Select DC...</option>');
                        }
                      });
                    }
                }
            });

            $.ajax({
                url: url,
                data: {'reportingDesignation': 'reportingDesignation'},
                success: function (data) {
                    $("#inputReportingDesignation2").html(data);
                    $('#inputReportingDesignation2').prop('selectedIndex', $('#inputReportingDesignation2 option[value=" ' +$('#objectInputReportingDesignation2').text()+ '"]').index());
                    $("#inputReportingDesignation2").removeAttr('disabled', 'disabled');
                    $("#inputReportingDesignation2").attr('required', true);
                    if ($('#objectInputReportingDesignation2').text()){
                      $.ajax({
                        url: url,
                        data: {'reportingOfficer': $('#objectInputReportingDesignation2').text()},
                        success: function (data) {
                            $("#inputReportingOfficer2").html(data);
                            if($('#inputReportingOfficer2').children('option').length > 1){
                                $('#inputReportingOfficer2').prop('selectedIndex', $('#inputReportingOfficer2 option[value=" ' +$('#objectInputReportingOfficer2').text()+ '"]').index());
                                $("#inputReportingOfficer2").removeAttr('disabled', 'disabled');
                                $("#inputReportingOfficer2").attr('required', true);
                            }
                            else{
                                $("#inputReportingOfficer2").attr('disabled', 'disabled');
                                $("#inputReportingOfficer2").removeAttr('required', 'required');
                            }
                        }
                      });
                    }
                }
            });

            $.ajax({
                url: url,
                data: {'functionDesignation': 'functionDesignation'},
                success: function (data) {
                    $("#inputDesignation2").html(data);
                    $('#inputDesignation2').prop('selectedIndex', $('#inputDesignation2 option[value="' +$('#objectInputDesignation2').text()+ '"]').index());
                    $("#inputDesignation2").removeAttr('disabled', 'disabled');
                    $("#inputDesignation2").attr('required', true);
                }
            });

            $.ajax({
                url: url,
                data: {'function': 'function'},
                success: function (data) {
                    $("#inputFunction2").html(data);
                    $('#inputFunction2').prop('selectedIndex', $('#inputFunction2 option[value="' +$('#objectInputFunction2').text()+ '"]').index());
                    $("#inputFunction2").removeAttr('disabled', 'disabled');
                    $("#inputFunction2").attr('required', true);
                }
            });
        }
    });


    $("#inputRegion").change(function () {
      var url = $("#taggingForm").attr("data-branches-url");
      var circleId = $(this).val();
      $.ajax({
        url: url,
        data: {'circle': circleId},
        success: function (data) {
            $("#inputRegionVal").val($("#inputRegion option:selected" ).text());
            $("#inputCircle").html(data);
            $("#inputhrManagerVal").val($($(".RegionEmpName")[0]).val());
            $("#inputhrManager" ).val($($(".RegionEmpCode")[0]).val());
            if($('#inputCircle').children('option').length > 4){$("#inputCircle").removeAttr('disabled', 'disabled');}
            else{
                $("#inputCircle").attr('disabled', 'disabled');
                $("#inputDivision").attr('disabled', 'disabled');
                $("#inputSubDivision").attr('disabled', 'disabled');
                $("#inputDC").attr('disabled', 'disabled');
            }
            $("#inputDivision").html('<option value="" selected>Select Division...</option>');
            $("#inputSubDivision").html('<option value="" selected>Select SubDivision...</option>');
            $("#inputDC").html('<option value="" selected>Select DC...</option>');
        }
      });
    });

    $("#inputCircle").change(function () {
      var url = $("#taggingForm").attr("data-branches-url");
      var divisionId = $(this).val();
      $.ajax({
        url: url,
        data: {'division': divisionId},
        success: function (data) {
            $("#inputCircleVal").val($("#inputCircle option:selected" ).text());
            $("#inputDivision").html(data);
            $("#inputhrManagerVal").val($($(".CircleEmpName")[0]).val());
            $("#inputhrManager" ).val($($(".CircleEmpCode")[0]).val());
            if($('#inputDivision').children('option').length > 4){$("#inputDivision").removeAttr('disabled', 'disabled');}
            else{
                $("#inputDivision").attr('disabled', 'disabled');
                $("#inputSubDivision").attr('disabled', 'disabled');
                $("#inputDC").attr('disabled', 'disabled');
            }
            $("#inputSubDivision").html('<option value="" selected>Select SubDivision...</option>');
            $("#inputDC").html('<option value="" selected>Select DC...</option>');
        }
      });
    });

    $("#inputDivision").change(function () {
      var url = $("#taggingForm").attr("data-branches-url");
      var subDivisionId = $(this).val();
      $.ajax({
        url: url,
        data: {'subDivision': subDivisionId},
        success: function (data) {
            $("#inputDivisionVal").val($("#inputDivision option:selected" ).text());
            $("#inputSubDivision").html(data);
            if($('#inputSubDivision').children('option').length > 1){$("#inputSubDivision").removeAttr('disabled', 'disabled');}
            else{
                $("#inputSubDivision").attr('disabled', 'disabled');
                $("#inputDC").attr('disabled', 'disabled');
            }
            $("#inputDC").html('<option value="" selected>Select DC...</option>');
        }
      });
    });

    $("#inputSubDivision").change(function () {
      var url = $("#taggingForm").attr("data-branches-url");
      var dcId = $(this).val();
      $.ajax({
        url: url,
        data: {'dc': dcId},
        success: function (data) {
            $("#inputSubDivisionVal").val($("#inputSubDivision option:selected" ).text());
            $("#inputDC").html(data);
            if($('#inputDC').children('option').length > 1){$("#inputDC").removeAttr('disabled', 'disabled');}
            else{
                $("#inputSubDivision").attr('disabled', 'disabled');
                $("#inputDC").attr('disabled', 'disabled');
            }
        }
      });
    });

    $("#inputDC").change(function () {
        $("#inputDCVal").val($("#inputDC option:selected").text());
    });

    $("#inputReportingDesignation").change(function () {
      var url = $("#taggingForm").attr("data-branches-url");
      var reportingOfficerId = $(this).val();
      $.ajax({
        url: url,
        data: {'reportingOfficer': reportingOfficerId},
        success: function (data) {
            $("#inputReportingOfficer").html(data);
            if($('#inputReportingOfficer').children('option').length > 1){
                $("#inputReportingOfficer").removeAttr('disabled', 'disabled');
                $("#inputReportingOfficer").attr('required', true);
            }
            else{
                $("#inputReportingOfficer").attr('disabled', 'disabled');
                $("#inputReportingOfficer").removeAttr('required', 'required');
            }
        }
      });
    });

    $("#inputReportingOfficer").change(function () {
        $("#inputReportingOfficerVal").val($("#inputReportingOfficer option:selected" ).text());
    });

    $("#inputReviewingDesignation").change(function () {
      var url = $("#taggingForm").attr("data-branches-url");
      var reviewingOfficerId = $(this).val();
      $.ajax({
        url: url,
        data: {'reportingOfficer': reviewingOfficerId},
        success: function (data) {
            $("#inputReviewing").html(data);
            if($('#inputReviewing').children('option').length > 1){
                $("#inputReviewing").removeAttr('disabled', 'disabled');
                $("#inputReviewing").attr('required', true);
            }
            else{
                $("#inputReviewing").attr('disabled', 'disabled');
                $("#inputReviewing").attr('required', false);
            }
        }
      });
    });

    $("#inputReviewing").change(function () {
        $("#inputReviewingVal").val($("#inputReviewing option:selected" ).text());
    });

    $("#inputAcceptingDesignation").change(function () {
      var url = $("#taggingForm").attr("data-branches-url");
      var acceptingOfficerId = $(this).val();
      $.ajax({
        url: url,
        data: {'reportingOfficer': acceptingOfficerId},
        success: function (data) {
            $("#inputAcceptingOfficer").html(data);
            if($('#inputAcceptingOfficer').children('option').length > 1){
                $("#inputAcceptingOfficer").removeAttr('disabled', 'disabled');
                $("#inputAcceptingOfficer").attr('required', true);
            }
            else{
                $("#inputAcceptingOfficer").attr('disabled', 'disabled');
                $("#inputAcceptingOfficer").attr('required', false);
            }
        }
      });
    });

    $("#inputAcceptingOfficer").change(function () {
        $("#inputAcceptingOfficerVal").val($("#inputAcceptingOfficer option:selected" ).text());
    });

    //Employee Tagging 1 Methods


    $("#inputRegion2").change(function () {
      var url = $("#taggingForm").attr("data-branches-url");
      var circleId = $(this).val();
      $.ajax({
        url: url,
        data: {'circle': circleId},
        success: function (data) {
            $("#inputCircle2").html(data);
            $("#inputhrManagerVal2").val($($(".RegionEmpName")[1]).val());
            $("#inputhrManager2" ).val($($(".RegionEmpCode")[1]).val());
            if($('#inputCircle2').children('option').length > 4){$("#inputCircle2").removeAttr('disabled', 'disabled');}
            else{
                $("#inputCircle2").attr('disabled', 'disabled');
                $("#inputDivision2").attr('disabled', 'disabled');
                $("#inputSubDivision2").attr('disabled', 'disabled');
                $("#inputDC2").attr('disabled', 'disabled');
            }
            $("#inputDivision2").html('<option value="" selected>Select Division...</option>');
            $("#inputSubDivision2").html('<option value="" selected>Select SubDivision...</option>');
            $("#inputDC2").html('<option value="" selected>Select DC...</option>');
            $("#inputRegionVal2").val($("#inputRegion2 option:selected" ).text());
        }
      });
    });

    $("#inputCircle2").change(function () {
      var url = $("#taggingForm").attr("data-branches-url");
      var divisionId = $(this).val();
      $.ajax({
        url: url,
        data: {'division': divisionId},
        success: function (data) {
            $("#inputCircleVal2").val($("#inputCircle2 option:selected" ).text());
            $("#inputDivision2").html(data);
            $("#inputhrManagerVal2").val($($(".CircleEmpName")[1]).val());
            $("#inputhrManager2" ).val($($(".CircleEmpCode")[1]).val());
            if($('#inputDivision2').children('option').length > 4){$("#inputDivision2").removeAttr('disabled', 'disabled');}
            else{
                $("#inputDivision2").attr('disabled', 'disabled');
                $("#inputSubDivision2").attr('disabled', 'disabled');
                $("#inputDC2").attr('disabled', 'disabled');
            }
            $("#inputSubDivision2").html('<option value="" selected>Select SubDivision...</option>');
            $("#inputDC2").html('<option value="" selected>Select DC...</option>');
        }
      });
    });

    $("#inputDivision2").change(function () {
      var url = $("#taggingForm").attr("data-branches-url");
      var subDivisionId = $(this).val();
      $.ajax({
        url: url,
        data: {'subDivision': subDivisionId},
        success: function (data) {
            $("#inputDivisionVal2").val($("#inputDivision2 option:selected" ).text());
            $("#inputSubDivision2").html(data);
            if($('#inputSubDivision2').children('option').length > 1){$("#inputSubDivision2").removeAttr('disabled', 'disabled');}
            else{
                $("#inputSubDivision2").attr('disabled', 'disabled');
                $("#inputDC2").attr('disabled', 'disabled');
            }
            $("#inputDC2").html('<option value="" selected>Select DC...</option>');
        }
      });
    });

    $("#inputSubDivision2").change(function () {
      var url = $("#taggingForm").attr("data-branches-url");
      var dcId = $(this).val();
      $.ajax({
        url: url,
        data: {'dc': dcId},
        success: function (data) {
            $("#inputSubDivisionVal2").val($("#inputSubDivision2 option:selected" ).text());
            $("#inputDC2").html(data);
            if($('#inputDC2').children('option').length > 1){$("#inputDC2").removeAttr('disabled', 'disabled');}
            else{
                $("#inputSubDivision2").attr('disabled', 'disabled');
                $("#inputDC2").attr('disabled', 'disabled');
            }
        }
      });
    });

    $("#inputDC2").change(function () {
        $("#inputDCVal2").val($("#inputDC2 option:selected").text());
    });

    $("#inputReportingDesignation2").change(function () {
      var url = $("#taggingForm").attr("data-branches-url");
      var reportingOfficerId = $(this).val();
      $.ajax({
        url: url,
        data: {'reportingOfficer': reportingOfficerId},
        success: function (data) {
            $("#inputReportingOfficer2").html(data);
            if($('#inputReportingOfficer2').children('option').length > 1){
                $("#inputReportingOfficer2").removeAttr('disabled', 'disabled');
                $("#inputReportingOfficer2").attr('required', true);
            }
            else{
                $("#inputReportingOfficer2").attr('disabled', 'disabled');
                $("#inputReportingOfficer2").removeAttr('required', 'required');
            }
        }
      });
    });

    $("#inputReportingOfficer2").change(function () {
        $("#inputReportingOfficerVal2").val($("#inputReportingOfficer2 option:selected" ).text());
    });

    $("#inputReviewingDesignation2").change(function () {
      var url = $("#taggingForm").attr("data-branches-url");
      var reviewingOfficerId = $(this).val();
      $.ajax({
        url: url,
        data: {'reportingOfficer': reviewingOfficerId},
        success: function (data) {
            $("#inputReviewing2").html(data);
            if($('#inputReviewing2').children('option').length > 1){
                $("#inputReviewing2").removeAttr('disabled', 'disabled');
                $("#inputReviewing2").attr('required', true);
            }
            else{
                $("#inputReviewing2").attr('disabled', 'disabled');
                $("#inputReviewing2").attr('required', false);
            }
        }
      });
    });

    $("#inputReviewing2").change(function () {
        $("#inputReviewingVal2").val($("#inputReviewing2 option:selected" ).text());
    });

    $("#inputAcceptingDesignation2").change(function () {
      var url = $("#taggingForm").attr("data-branches-url");
      var acceptingOfficerId = $(this).val();
      $.ajax({
        url: url,
        data: {'reportingOfficer': acceptingOfficerId},
        success: function (data) {
            $("#inputAcceptingOfficer2").html(data);
            if($('#inputAcceptingOfficer2').children('option').length > 1){
                $("#inputAcceptingOfficer2").removeAttr('disabled', 'disabled');
                $("#inputAcceptingOfficer2").attr('required', true);
            }
            else{
                $("#inputAcceptingOfficer2").attr('disabled', 'disabled');
                $("#inputAcceptingOfficer2").attr('required', false);
            }
        }
      });
    });

    $("#inputAcceptingOfficer2").change(function () {
        $("#inputAcceptingOfficerVal2").val($("#inputAcceptingOfficer2 option:selected" ).text());
    });

    //Employee Tagging 2 Methods

    $("#addAnotherAppraisee").click(function () {
      var url = $("#taggingForm").attr("data-branches-url");
      $("#taggingPart2").css('display', 'table');
      $("#addAnotherAppraiseeDiv").css('display', 'none');
      $("#delAnotherTaggingDiv").css('display', 'block');
      $('#submitBtn').attr('disabled', 'disabled');

      $("#isAnotherAppraise").prop("checked", true);
      $("#inputFromDate2").attr('required', true);
      $("#inputToDate2").attr('required', true);
      $("#inputRegion2").attr('required', true);
      $("#inputReportingDesignation2").attr('required', true);
      $("#inputFunction2").attr('required', true);
      $("#inputDesignation2").attr('required', true);

      $.ajax({
            url: url,
            data: {'region': 'region'},
            success: function (data) {
                $("#inputRegion2").html(data);
                if($('#objectInputRegion2').text()){
                    $('#inputRegion2').prop('selectedIndex', $('#inputRegion2 option[value=" ' +$('#objectInputRegion2').text()+ '"]').index());
                    const date = new Date($('#objectFromDate2').text());
                    var result = date.setDate(date.getDate() + 1);
                    $('#inputFromDate2').val(new Date(result).toISOString().split('T')[0]);
                    const date2 = new Date($('#objectToDate2').text());
                    var result2 = date2.setDate(date2.getDate() + 1);
                    $('#inputToDate2').val(new Date(result2).toISOString().split('T')[0]);
                    $('#inputRemark2').val($('#objectRemark2').text());
                }
            }
      });
      $.ajax({
          url: url,
          data: {'reportingDesignation': 'reportingDesignation'},
          success: function (data) {
              $("#inputReportingDesignation2").html(data);
              $('#inputReportingDesignation2').prop('selectedIndex', $('#inputReportingDesignation2 option[value=" ' +$('#objectInputReportingDesignation2').text()+ '"]').index());
              $("#inputReportingDesignation2").removeAttr('disabled', 'disabled');
              $("#inputReportingDesignation2").attr('required', true);
          }
      });
      $.ajax({
          url: url,
          data: {'functionDesignation': 'functionDesignation'},
          success: function (data) {
              $("#inputDesignation2").html(data);
              $('#inputDesignation2').prop('selectedIndex', $('#inputDesignation2 option[value="' +$('#objectInputDesignation2').text()+ '"]').index());
              $("#inputDesignation2").removeAttr('disabled', 'disabled');
              $("#inputDesignation2").attr('required', true);
          }
      });
      $.ajax({
          url: url,
          data: {'function': 'function'},
          success: function (data) {
              $("#inputFunction2").html(data);
              $('#inputFunction2').prop('selectedIndex', $('#inputFunction2 option[value="' +$('#objectInputFunction2').text()+ '"]').index());
              $("#inputFunction2").removeAttr('disabled', 'disabled');
              $("#inputFunction2").attr('required', true);
          }
      });
    });

    $("#delAnotherTagging").click(function () {
      $("#taggingPart2").css('display', 'none');
      $("#addAnotherAppraiseeDiv").css('display', 'block');
      $("#delAnotherTaggingDiv").css('display', 'none');

      $("#isAnotherAppraise").prop("checked", false);
      $('#submitBtn').removeAttr('disabled');
      $("#inputFromDate2").removeAttr('required', false);
      $("#inputToDate2").removeAttr('required', false);
      $("#inputRegion2").removeAttr('required', false);
      $("#inputReportingDesignation2").removeAttr('required', false);
      $("#inputFunction2").removeAttr('required', false);
      $("#inputDesignation2").removeAttr('required', false);
      $("#inputRemark2").removeAttr('required', false);
      $("#reportingOfficerCode2").removeAttr('required', false);
      $("#inputReportingOfficer2").removeAttr('required', false);

      $("#inputFunction2").val('');
      $("#inputDesignation2").val('');
      $("#inputRegion2").val('');
      $("#inputRegionVal2").val('');
      $("#inputCircleVal2").val('');
      $("#inputDivisionVal2").val('');
      $("#inputSubDivisionVal2").val('');
      $("#inputDCVal2").val('');
      $("#inputFromDate2").val('');
      $("#inputToDate2").val('');
      $("#inputReportingDesignation2").val('');
      $("#inputReportingOfficer2").val('');
      $("#inputReportingOfficerVal2").val('');
      $("#inputRemark2").val('');

    });

