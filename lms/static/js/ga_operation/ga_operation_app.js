;(function (define) {

    define(['backbone'], function(Backbone) {
        'use strict';

        return function (GaOperationRouter, GaBaseView, MoveVideos, CreateCerts, CreateCertsMeeting, PublishCerts,
                         MutualGradingReport, DiscussionData, PastGraduatesInfo, LastLoginInfo, AggregateG1528) {
            var gaOperationRouter = new GaOperationRouter();
            var gabaseView = new GaBaseView();
            var moveVideos = new MoveVideos();
            var createCerts = new CreateCerts();
            var createCerts_meeting = new CreateCertsMeeting();
            var publishCerts = new PublishCerts();
            var mutualGrading_report = new MutualGradingReport();
            var discussionData = new DiscussionData();
            var pastGraduatesInfo = new PastGraduatesInfo();
            var lastLoginInfo = new LastLoginInfo();
            var aggregateG1528 = new AggregateG1528();
        };

    });

})(define || RequireJS.define);