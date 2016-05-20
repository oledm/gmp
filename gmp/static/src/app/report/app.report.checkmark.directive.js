(function() {
    'use strict';

    angular.module('app.report')
        .directive('checkmark', CheckmarkDirective)
        .directive('datePicker', DatePicker);

    function DatePicker(uibDatepickerPopupConfig) {
        'ngInject';

        function controller() {
            var vm = this;

            uibDatepickerPopupConfig.closeText = 'Закрыть';
            uibDatepickerPopupConfig.currentText = 'Сегодня';
            uibDatepickerPopupConfig.clearText = 'Очистить';
            uibDatepickerPopupConfig.type = 'month';

            vm.dateOptions = {
                startingDay: 1
            };

            vm.yearOptions = {
                datepickerMode: 'year',
                maxMode: 'year',
                minMode: 'year',
                formatYear: 'yyyy'
            };

            vm.open = function() {
              vm.popup.opened = true;
            };

            vm.popup = {
              opened: false
            };
        }

        function link (scope, elem, attrs, formController) {
            var field = formController.$name + '.' + 'order_date';
            var input = angular.element(elem.find('input'));
            scope.$parent.$watch(`${field}.$invalid && ${field}.$touched`, function(newValue) {
                console.log('valid', newValue);
                elem.toggleClass('has-error', newValue);
            });
            scope.$watch(scope.model, () => {
                console.log('GFFFFGGGGG');
            });
            input.on('keyup', () => {
                console.log('fdfdfd');
//                $timeout(() => angular.element('#mainForm').trigger('change'), 0);
            });

        }

        return {
            controller: controller,
            controllerAs: 'vm',
            restrict: 'E',
            require: '^form',
            scope: {
                name: '@',
                model: '=ngModel',
            },
            template: `
                  <label class="control-label" for="{{name}}"></label>
                  <p class="input-group">
                      <input type="text" required ng-model="model" id="{{name}}" name="{{name}}"
                      class="form-control" ng-model-options="{timezone: 'UTC'}" is-open="vm.popup.opened" />
                      <span class="input-group-btn">
                        <button type="button" class="btn btn-default" ng-click="vm.open()">
                        <i class="glyphicon glyphicon-calendar"></i></button>
                      </span>
                  </p>
                  <div class="help-block" role="alert" ng-messages="vm.orderForm.order_date.$error" ng-if="vm.orderForm.order_date.$touched">
                      <div ng-messages-include="/static/src/assets/messages.html"></div>
                  </div>
            `,
            compile: function(tElem, tAttrs) {
                var label = angular.element(tElem.find('label')),
                    input = angular.element(tElem.find('input'));
                label.html(tAttrs.label);
                if (tAttrs.mode === 'year') {
                    input.attr({
                        'datepicker-options': 'vm.yearOptions',
                        'uib-datepicker-popup': 'yyyy'
                    });
                } else {
                    input.attr({
                        'datepicker-options': 'vm.dateOptions',
                        'uib-datepicker-popup': 'dd MMMM yyyy'
                    });

                }
                return link;
            }
        }
    }

    function CheckmarkDirective() {

        return {
            require: '^form',
            restrict: 'A',
            link: function(scope, elem, attrs, formController) {
                if (attrs.validOn !== undefined) {
                    attrs.$observe('validOn', function(newValue) {
                        newValue = scope.$eval(newValue)
                        setCheckMark(newValue);
                    });
                } else {
                    scope.$watch(formController.$name + '.$valid', function(newValue) {
                        setCheckMark(newValue);
                    });
                }
                ///////////////////////////////////////////////////
                function setCheckMark(value) {
                    if (value) {
                        scope.showCheckmark = true;
                    } else {
                        scope.showCheckmark = false;
                    }
                }

            },
            scope: true,
            transclude: true,
            template: '<span ng-if="showCheckmark">' +
                '<i class="glyphicon glyphicon-ok" style="color: #00e676"></i>&nbsp;' +
                '</span>' +
                '<span ng-transclude></span>'
        };
    }
})();
