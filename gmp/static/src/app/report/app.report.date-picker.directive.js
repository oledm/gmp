(function() {
    'use strict';

    angular.module('app.report')
        .directive('watcher', Watcher);
//        .directive('datePicker', DatePicker2);

    function Watcher() {
        return {
            restrict: 'A',
            link: function(scope, elem, attrs) {
                var target = attrs.ngModel ? attrs.ngModel : attrs.watcher;

                if (angular.isUndefined(target)) {
                    return;
                }

                scope.$watch(target, (newVal) => {
                    if (newVal) {
                        elem.trigger('change');
                    }
                });
            }
        }
    }

//            '<input type="text" ng-model="vm.model" name="vm.name" />' + 
//            '<div ng-messages="vm.$error" role="alert">' +
//              '<div ng-messages-include="/static/src/assets/messages.html"></div>' +
//            '</div>',
    function DatePicker2(uibDatepickerPopupConfig) {
      function link(scope, elem, attrs, ctrls) {
          var ngModel = ctrls[0];
          var datePicker = ctrls[1];
          datePicker.name = attrs.name;
          datePicker.label = attrs.label;
          datePicker.setModel(ngModel);
      }

      return {
        restrict: 'E',
        template: `
                    <label ng-class="{ 'has-error': true }" class="control-label" for="vm.name">{{vm.label}}</label>
                      <p class="input-group">
                    
                          <input type="text" ng-model="vm.model" id="vm.name" name="vm.name"
                          class="form-control" ng-model-options="{timezone: 'UTC'}"
                            datepicker-options="dc.dateOptions"  uib-datepicker-popup="dd MMMM yyyy"
                          is-open="vm.popup.opened" />
                    
                          <span class="input-group-btn">
                            <button type="button" class="btn btn-default" ng-click="vm.open()">
                            <i class="glyphicon glyphicon-calendar"></i></button>
                          </span>
                    
                      </p>
                      
                        <div ng-messages="vm.$error" role="alert">
                          <div ng-messages-include="/static/src/assets/messages.html"></div>
                        </div>
                  `,
        transclude: true,
        scope: {},
        require: ['ngModel', 'datePicker'],
        link: link,
        controllerAs: 'vm',
        controller: function($scope) {
            var vm = this;
            
            vm.model = null;
            vm.setModel = setModel;

            function setModel(ngModel) {
                vm.$error = ngModel.$error;
                vm.$touched = ngModel.$touched;
                console.log('touched:', vm.$touched);
                
                ngModel.$render = function() {
                    vm.model = ngModel.$viewValue;
                };
                
                $scope.$watch('vm.model', function(newval) {
                    ngModel.$setViewValue(newval);
                });

                $scope.$watch('ngModel.$touched', function(newval) {
                    console.log('touched:', vm.$touched);
                });

                //////////////////////////////////////////

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
                    console.log('open');
                  vm.popup.opened = true;
                };

                vm.popup = {
                  opened: false
                };
            }
        }
    }

    }

    function DatePicker($compile, $timeout, uibDatepickerPopupConfig) {
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
            var field = formController.$name + '.' + scope.name;
            var divMessages = angular.element(elem.find('.contttttttt'));

            scope.$parent.$watch(`${field}.$invalid && ${field}.$touched`, function(newValue) {
                elem.toggleClass('has-error', newValue);
                toggleMessages(newValue);
            });

//            scope.$parent.$watch(`${field}.$touched`, function(newValue) {
//                toggleMessages(newValue);
//            });

            scope.$parent.$watch(`${field}.$error`, function(newValue) {
                var val = JSON.stringify(newValue);
                console.log('error', val);
                var messages = `<div class='help-block' role='alert' ng-messages='{required: true}'>
                    <div ng-messages-include="/static/src/assets/messages.html"></div>
                </div>`;
//                divMessages.empty();
//                divMessages.html(angular.element($compile(messages)(scope)));
//                divMessages.empty();

//                var newDiv = divMessages.clone();
//                newDiv.html(angular.element($compile(messages)(scope)));
//                divMessages.html(newDiv);

                var newDiv = angular.element($compile(messages)(scope));
                divMessages.replaceWith(newDiv);

//                divMessages.append(angular.element($compile(messages)(scope)));
//                $compile(divMessages)(scope);
            }, true);

            scope.$watch(() => scope.model, (newVal, oldVal) => {
                if (newVal !== oldVal) {
                    // Trigger change event for potential listener - saveHistory directive
                    elem.trigger('change');
                }
            });

            function toggleMessages(value) {
                if (value === true) {
                    divMessages.show();
                } else {
                    divMessages.hide();
                }
            }
        }

        return {
            controller: controller,
            controllerAs: 'vm',
            restrict: 'E',
            priority: 1,
            require: '^form',
            scope: {
                name: '@',
                model: '=ngModel',
            },
            template: `
                  <label class="control-label" for="{{name}}"></label>
                  <p class="input-group">

                      <input type="text" required ng-model="model" id="{{name}}" name="{{name}}"
                      class="form-control" ng-model-options="{timezone: 'UTC'}"
                      is-open="vm.popup.opened" />

                      <span class="input-group-btn">
                        <button type="button" class="btn btn-default" ng-click="vm.open()">
                        <i class="glyphicon glyphicon-calendar"></i></button>
                      </span>

                      <div class="contttttttt"></div>


                  </p>

            `,
            compile: function(tElem, tAttrs) {
                var label = angular.element(tElem.find('label')),
                    input = angular.element(tElem.find('input')),
//                    messages = angular.element(tElem.find('div.help-block')),
                    form_name = angular.element(tElem.closest('ng-form')).attr('name'),
                    input_error = `${form_name}.${tAttrs.name}.$error`;

                label.html(tAttrs.label);

//                console.log('Form name is', form_name);
                console.log('validation_name', input_error);
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
//                var messages = '<div class="help-block" role="alert" ng-messages="' + input_error + '">' +
//                      '<div ng-messages-include="/static/src/assets/messages.html"></div>' +
//                  '</div>';
//                tElem.append(angular.element(messages));
//                messages.attr('ng-messages', input_error);
                return link;
            }
        }
    }
})();
