$(function(){
/*
    $(".alert-box").fadeTo(2000, 500).slideUp(500, function(){
        $(this).slideUp(500);

    });*/
    var url = document.location.toString();
    if (url.match('#')) {
        $('.nav-tabs a[href="#' + url.split('#')[1] + '"]').tab('show');
    }
    $('.alert[data-auto-dismiss]').each(function (index, element) {
        var $element = $(element),
            timeout  = $element.data('auto-dismiss') || 5000;

        setTimeout(function () {
            $element.alert('close');
        }, timeout);
    });
    $('#example').DataTable({
        paging: false,
        searching: false
    });
     var container = document.getElementById("jsoneditor");
    console.log(container);
    var editor = new JSONEditor(container, {
        modes: ['code', 'form', 'text', 'tree', 'view'],
        onChange: function(){
            var json = editor.get();
            $("#id_params").val(JSON.stringify(json));
        }
    });
    if($("#id_params").val() !== "") {

        editor.set(JSON.parse($("#id_params").val()));
    }

     var tcontainer = document.getElementById("tjsoneditor");
    console.log(tcontainer);
    var teditor = new JSONEditor(tcontainer, {
        modes: ['code', 'form', 'text', 'tree', 'view'],
        onChange: function(){
            var json = teditor.get();
            $("#id_tparams").val(JSON.stringify(json));
        }
    });
    if($("#id_tparams").val() !== "") {
        teditor.set(JSON.parse($("#id_tparams").val()));
    }

});
var underscore = angular.module('underscore', []);
underscore.factory('_', ['$window', function($window) {
  return $window._; // assumes underscore has already been loaded on the page
}]);
var app = angular.module('tohkenApp', ['ngSanitize', 'underscore', 'ui.bootstrap', 'angularFileUpload']);
app.config(['$httpProvider', function($httpProvider) {
    //initialize get if not there
    if (!$httpProvider.defaults.headers.get) {
        $httpProvider.defaults.headers.get = {};
    }

    // Answer edited to include suggestions from comments
    // because previous version of code introduced browser-related errors

    //disable IE ajax request caching
    $httpProvider.defaults.headers.get['If-Modified-Since'] = 'Mon, 26 Jul 1997 05:00:00 GMT';
    // extra
    $httpProvider.defaults.headers.get['Cache-Control'] = 'no-cache';
    $httpProvider.defaults.headers.get['Pragma'] = 'no-cache';
}]);
app.controller('furnanceCtrl', function($scope, $http, _) {
  $scope.firstName = "John";
  $scope.lastName = "Doe";
    $scope.values = {};
    $http.get(loadJFUrl).then(function(res){
        console.log(res.data);
        $scope.furnanceJobs = res.data;

    });
    $http.get(furnanceListUrl, {cache:false}).then(function(res){
        $scope.furnance_list = res.data;
        console.log($scope.furnance_list)
    });
  $scope.fullName = function() {
    return $scope.firstName + " " + $scope.lastName;
  };
    $scope.save = function(data) {
        console.log(data);
        var package = {action:"save", data: data};
        $http.post(loadJFUrl, package).then(function(res){
            console.log(res);

            BootstrapDialog.show({
                message: 'Save Success'
            });
        });
    };
    $scope.batchActive = function(n, n_is_active){
        console.log($scope.furnance_list);
        console.log(n);
        n.batch_options = _.filter($scope.furnance_list, function(o){

            var res  = o.furnance.split('-');
            var fp = res[0];
            console.log(res);
            console.log(n.furnance__furnance);
            if( fp == n.furnance__furnance.split('-')[0] )
                return o;
        });
        console.log(n.batch_options);
    };
	$scope.toggleSelection = function(n, furnance) {
        if( n.batch_values == undefined  ) {
            n.batch_values = [];
        }
		var idx = n.batch_values.indexOf(furnance);

		// Is currently selected
		if (idx > -1) {
			n.batch_values.splice(idx, 1);
		}

		// Is newly selected
		else {
			n.batch_values.push(furnance);
		}
	};
    $scope.delete = function(data) {
        console.log(data);
        var package = {action:"delete", data: data};
        var deleteConfirm =  confirm("Are you sure ?");
        if( deleteConfirm ) {
            $http.post(loadJFUrl, package).then(function(res){
                location.reload();
            });
        }
    };
})
    .controller('SettingCtrl', function($scope, $http, _, $interval, $timeout, FileUploader) {
        $scope.model = {};
        $scope.msg = {};

        $scope.batch_params = [
            {key: 'sm', text: 'SM299224-0010'},
            {key: 'wax', text: 'Lost wax 6 Dan'},
            {key: 'support_ami', text: 'Support net ami'},
            {key: 'plate', text: 'Plate คั่นงาน'},
            {key: 'under_ami', text: 'Under net ami'},
            {key: 'cover_ami', text: 'Cover net ami'},
        ];

        $scope.createSettingPhoto = function(setting, group) {

            $http.post(createSettingPhotoURL, {id: setting.id, group: group }).then(function(){
                    $scope.getSettingPhoto(setting);
                });
        };
        $scope.cal_total = function(cal_type){
            console.log($scope.model);
            if($scope.model !== null) {
                console.info(Object.entries($scope.model));
                if( cal_type == "batch" ) {
                    var sum = 0;
                    console.log("i cal");
                    $scope.batch_params.forEach(function(o){
                        if( $scope.model[o.key+"_total"]  != undefined )
                            sum += $scope.model[o.key+"_total"];
                    });
                    $scope.model.weight_total = sum;
                    return sum;
                }
            }
        };
        $scope.getSettingPhoto = function(setting) {
            $http.post(getSettingPhotoURL, {id: setting.id}).then(function(res){
                $scope.photos = res.data;
                $scope.jigSpecPhotos = _.filter(res.data, function(o){
                    if( o.group == "Jig Setting" )
                        return o;
                });
                $scope.settingPhotos = _.filter(res.data, function(o){
                    if( o.group == "Setting Method" )
                        return o;
                });
            });
        };
        $scope.deleteSetting = function(setting){
            if( confirm('Are you sure ?') ) {
                console.log("yes");
                $http.post(jobDeleteSettingURL, {id: setting.id}).then(function(){
                    $scope.$parent.getJobSettings();
                });
            }else {
                console.log("cancel");
            }
        };
        $scope.initCtrl = function(job, jsobj) {
            console.log("init call");
            console.info(job);
            console.info(jsobj);
            if ((job !== undefined ) && ( jsobj !== undefined )){
                $scope.job = job;
                $scope.model  = jsobj.values == null ? {} : jsobj.values;
                $scope.jsobj = jsobj;

                $scope.getSettingPhoto($scope.jsobj);

                var uploader = $scope.uploader = new FileUploader({
                    url: updateSettingPhotoURL,
                    autoUpload: true,
                    /*formData: [{id: $scope.jsobj.id }]*/
                });

                uploader.onCompleteItem = function(fileItem, response, status, headers) {
                    console.info('onCompleteItem', fileItem, response, status, headers);
                    $scope.getSettingPhoto($scope.jsobj);
                };

                $interval(function(){
                    console.log("interval call");
                    $scope.updateData();
                    $scope.updatePhotoData();
                },UPDATE_INTERVAL);
            }
        };
        $scope.updatePhotoData = function() {
            $scope.photos.forEach(function(value, index, array){
                $http.post(updateSettingPhotoDataURL, {id: value.id, data:{caption:value.caption}}).then(function(res){
                    console.info(res);
                },function(){
                    alert('error update phot data');
                });
            });
        };
        $scope.updateData = function(){

                //console.log($scope.jsobj.id, '=', $scope.model.total_weight);
                $scope.msg.show = true;
                $scope.msg.success = true;
                $scope.msg.message = "saving..";
                console.log($scope.model);
                if($scope.model !== null) {
                    $http.post(jobSettingURL, {id: $scope.jsobj.id, data: $scope.model }, {cache: false}).then(function(res){
                        console.log("values save !!");
                        $timeout(function(){
                            $scope.msg.message = "&nbsp;&nbsp;";
                        },2000);

                    }, function(){
                        $scope.msg.success = false;
                        $scope.msg.message = "error saving";
                    });
                }
        };
        $scope.totalWeight = function() {
            if( ($scope.job !== undefined ) && (   $scope.model !== null)) {

                $scope.model.total_weight = $scope.model.total_row_hr * ( $scope.model.total_ami_weight + $scope.model.total_part_weight );
                console.log("Save data...");

                if( $scope.model.total_weight <= $scope.job.main_furnance__max_weight_value ) {
                    return $scope.model.total_weight;
                }else {
                    return "Over limit ("+$scope.model.total_weight+")";
                }
            }


        };
    })
    .controller('SbFormCtrl', function($scope, $http, _, $interval, $timeout, FileUploader) {
        $scope.model = {};
        $scope.msg = {};

        $http.get(furnanceListUrl).then(function(res){
            $scope.furnances = res.data;
        });
        $scope.mediaSize = function(furnance){
            console.log(furnance);
            if( furnance != null && furnance != undefined  && $scope.furnances != undefined){

                var theFur = _.filter($scope.furnances, function(o){
                    if( o.furnance == furnance )
                        return o;
                });
                //console.log(theFur);
                return theFur[0].qcol1;
            }

        };

        $scope.createSbPhoto = function(sb, group) {

            $http.post(createSbPhotoURL, {id: sb.id, group: group }).then(function(){
                    $scope.getSbPhoto(sb);
                });
        };
        $scope.getSbPhoto = function(sb) {
            $http.post(getSbPhotoURL, {id: sb.id}).then(function(res){
                $scope.photos = res.data;
                console.log($scope.photos);
                $scope.settingPhotos = _.filter(res.data, function(o){
                    if( o.group == "Setting" )
                        return o;
                });
                $scope.usagePhotos = _.filter(res.data, function(o){
                    if( o.group == "Usage" )
                        return o;
                });
            });
        };
        $scope.deleteSb = function(setting){
            if( confirm('Are you sure ?') ) {
                console.log("yes");
                $http.post(sbDeleteURL, {id: setting.id}).then(function(){
                    $scope.$parent.getSbs();
                });
            }else {
                console.log("cancel");
            }
        };
        $scope.initCtrl = function(job, jsobj) {
            console.info(job, jsobj)
            if ((job !== undefined ) && ( jsobj !== undefined )){
                $scope.job = job;
                $scope.model  = jsobj.values == null ? {} : jsobj.values;
                $scope.jsobj = jsobj;

                $scope.getSbPhoto($scope.jsobj);

                var uploader = $scope.uploader = new FileUploader({
                    url: sbPhotoUploadURL,
                    autoUpload: true,
                    /*formData: [{id: $scope.jsobj.id }]*/
                });

                uploader.onCompleteItem = function(fileItem, response, status, headers) {
                    console.info('onCompleteItem', fileItem, response, status, headers);
                    $scope.getSbPhoto($scope.jsobj);
                };

                $interval(function(){
                    console.log("interval call");
                    $scope.updateData();
                    $scope.updatePhotoData();
                },UPDATE_INTERVAL);
            }
        };
        $scope.updatePhotoData = function() {
            $scope.photos.forEach(function(value, index, array){
                $http.post(sbPhotoDataURL, {id: value.id, data:{caption:value.caption}}).then(function(res){
                    console.info(res);
                },function(){
                    alert('error update phot data');
                });
            });
        };
        $scope.updateData = function(){

                //console.log($scope.jsobj.id, '=', $scope.model.total_weight);
                $scope.msg.show = true;
                $scope.msg.success = true;
                $scope.msg.message = "saving..";
                console.log($scope.model);
                if($scope.model !== null) {
                    $http.post(sbApiURL, {id: $scope.jsobj.id, data: $scope.model }, {cache: false}).then(function(res){
                        console.log("values save !!");
                        $timeout(function(){
                            $scope.msg.message = "&nbsp;&nbsp;";
                        },2000);

                    }, function(){
                        $scope.msg.success = false;
                        $scope.msg.message = "error saving";
                    });
                }
        };
    })
    .controller('ExportDataCtrl', function($scope, $http, _, $interval, $timeout, FileUploader) {
        $scope.model = {};
        $scope.msg = {};

        $scope.init = function() {
            console.log("init");
            //list data
            reloadExportList();
        };
        $scope.templateMap = {
            "conveyor": "Conveyor",
            "batch-tvq-tfq": "Batch TVQ-TFQ",
            "batch-tgc-trgc": "Batch TGC-TRGC",
            "batch-tbt": "Batch TBT",
            "tsp-tsap": "TSP-TSAP",
            "tih": "TIH"
        };
        // generate excel
        $scope.generate = function() {
            //create excel file set, heat treatment, inspection, setting, shotblast
            var waitDialog = BootstrapDialog.show({
                message: 'Processing'
            });
            $http.post(exportDataURL).then(function(res){
                console.log("hello");
                waitDialog.close();
                BootstrapDialog.show({
                    message: 'Success'
                });
                reloadExportList();
            }, function(err){
                BootstrapDialog.show({
                    message: err,
                    type: BootstrapDialog.TYPE_ERROR
                });
            });
        };

        function reloadExportList() {
            $http.get(exportDataURL).then(function(res){
                $scope.exports = res.data;
            });
        };

    })
    .controller('ShotBlastCtrl', function($scope, $http, _) {
        $scope.sbForm = {};
        $scope.sbTypes = ["Drum", "Hanger"];
        $scope.createSB = function() {
            $http.post(createSbURL,{ data:  $scope.sbForm }).then(function(res){
                console.log(res);

                BootstrapDialog.show({
                    message: 'Save Success'
                });
                $scope.getSbs();
            });
        };
        $scope.getSbs = function() {
            console.log("get sbs");
            $http.get(sbListURL, {cache: false}).then(function(res){
                $scope.sbs = res.data;
            });
        };
        $http.get(jobGetURL, {cache:false}).then(function(res){
            $scope.job = res.data[0];
            console.log("job", $scope.job);
            $scope.getSbs();
            $http.get(loadJFUrl, {cache:false}).then(function(res){
                var furnanceJobs = res.data;
                $scope.mainValues = _.filter(furnanceJobs, function(o){
                    console.log(o);
                    if( o.furnance == $scope.job.main_furnance )
                        return o;
                });
            });
        });
    })
    .controller('TemplateFormCtrl', function($scope, $http, _){

        $scope.templateMap = {
            "conveyor": "Conveyor",
            "batch-tvq-tfq": "Batch TVQ-TFQ",
            "batch-tgc-trgc": "Batch TGC-TRGC",
            "batch-tbt": "Batch TBT",
            "tsp-tsap": "TSP-TSAP",
            "tih": "TIH"
        };
        $scope.getNumber = function(num) {
            return new Array(num);
        };
        $scope.selectTemplate = function(templateName) {
            $http.post(jobAddJfURL, {template: templateName})
                .then(function(res){
                    $scope.furnanceJobs = res.data;
                }, function(err){
                    alert("save job furnance error");
                });
        };

        $scope.model = {};
        $scope.save = function(data) {

            var package = {action:"save", data: data};
            $http.post(loadJFUrl, package).then(function(res){
                console.log(res);

                BootstrapDialog.show({
                    message: 'Save Success'
                });
            });
        };
        $scope.init = function() {
            furnanceList();
            loadData();
        };
        function furnanceList() {
            $http.get(furnanceListUrl, {cache:false}).then(function(res){
                $scope.furnance_list = res.data;
                console.log($scope.furnance_list)
            });
        }
        function loadData() {

            $http.get(loadJFUrl).then(function(res){
                console.log(res.data);
                $scope.furnanceJobs = res.data;

            });
        }
        $scope.selectFurnance = function(furnance_id, jobFurnance) {

            var package = {action:"updateFurnance", data: {id:jobFurnance.id, furnance_id: furnance_id}};
            $http.post(loadJFUrl, package).then(function(res){
                console.log(res);
                location.reload();
                BootstrapDialog.show({
                    message: 'Save Success'
                });
            });
        };
        $scope.deleteJf = function(data) {
            var package = {action:"delete", data: data};
            var deleteConfirm =  confirm("Are you sure ?");
            if( deleteConfirm ) {
                $http.post(loadJFUrl, package).then(function(res){
                    loadData();
                });
            }
        };
    })
    .controller('SetConveyorCtrl', function($scope, $http, _) {
        console.log("set con");
        $scope.msg = "hello";
        //$scope.model = {};
        $scope.settingForm = {};
        $scope.settingTypes = ["Conveyor", "Batch"];


        $scope.createSetting = function() {
            console.log("create setting");
            $http.post(jobcreateSettingURL,{ data:  $scope.settingForm }).then(function(res){
                console.log(res);

                BootstrapDialog.show({
                    message: 'Save Success'
                });
                $scope.getJobSettings();
            });
        };
        $scope.getJobSettings = function() {
            console.log("get jobs");
            $http.get(jobSettingURL, {cache: false}).then(function(res){
                $scope.jobSettings = res.data;
            });
        };
        $scope.getJobSettings();
        $scope.partAmtChange = function(){
           $scope.model.total_part_weight  = $scope.model.part_amt * $scope.job.part__kgperpc;
        };
        $scope.amiAmtChange = function(){
           $scope.model.total_ami_weight  = $scope.model.ami_wpc * $scope.model.ami_amt;
        };
        $scope.totalWeight = function() {
            if($scope.job !== undefined) {
                $scope.model.total_weight = $scope.model.total_row_hr * ( $scope.model.total_ami_weight + $scope.model.total_part_weight );
                console.log("Save data...");
                if( $scope.model.total_weight <= $scope.job.main_furnance__max_weight_value ) {
                    return $scope.model.total_weight;
                }else {
                    return "Over limit ("+$scope.model.total_weight+")";
                }
            }


        };
        $scope.lengthAmtChange = function(){
           $scope.model.total_row_hr   = $scope.model.nrow_hr * $scope.model.length_row;
        };
        $http.get(jobGetURL, {cache:false}).then(function(res){
            $scope.job = res.data[0];

            $http.get(loadJFUrl, {cache:false}).then(function(res){
                var furnanceJobs = res.data;
                $scope.mainValues = _.filter(furnanceJobs, function(o){
                    console.log(o);
                    if( o.furnance == $scope.job.main_furnance )
                        return o;
                });
            });
        });
    });
