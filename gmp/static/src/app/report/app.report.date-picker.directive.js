(function() {
    'use strict';

    angular.module('app.report')
        .directive('datePicker', DatePicker);

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

            scope.$parent.$watch(`${field}.$invalid && ${field}.$touched`, function(newValue) {
                elem.toggleClass('has-error', newValue);
            });

//            scope.$parent.$watch(`${field}.$error`, function(newValue) {
//                console.log('watch', newValue);
//                var messages = '<div class="help-block" role="alert" ng-messages="{{' + field + '.$error}}">' +
//                      '<div ng-messages-include="/static/src/assets/messages.html"></div>' +
//                  '</div>';
//                elem.append(angular.element($compile(messages)(scope)));
//            }, true);
            scope.$watch(() => scope.model, (newVal, oldVal) => {
                if (newVal !== oldVal) {
                    // Trigger change event for potential listener - saveHistory directive
                    elem.trigger('change');
                }
            });

            console.dir(formController[scope.name]);
            console.log(JSON.stringify(formController[scope.name].$error.required));
            console.dir(scope.$parent.$eval((`${field}.$error`)));
//            scope.$watch(formController[scope.name].$error, function(newValue) {
//                console.log(`error: ${JSON.stringify(newValue)}`);
//            });

        }

        return {
            controller: controller,
            controllerAs: 'vm',
            restrict: 'E',
//            priority: -1,
//            terminal: true,
            require: '^form',
            scope: {
                name: '@',
                model: '=ngModel',
            },
            template: `
                  <label class="control-label" for="{{name}}"></label>
                  <p class="input-group">

                      <input type="text" required ng-minlength="5" ng-model="model" id="{{name}}" name="{{name}}"
                      class="form-control" ng-model-options="{timezone: 'UTC'}"
                      is-open="vm.popup.opened" />

                      <span class="input-group-btn">
                        <button type="button" class="btn btn-default" ng-click="vm.open()">
                        <i class="glyphicon glyphicon-calendar"></i></button>
                      </span>


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
