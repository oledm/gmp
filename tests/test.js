xdescribe('angularjs homepage todo list', function() {
  it('should add a todo', function() {
    browser.get('https://angularjs.org');

    element(by.model('todoList.todoText')).sendKeys('write first protractor test');
    element(by.css('[value="add"]')).click();

    var todoList = element.all(by.repeater('todo in todoList.todos'));
    expect(todoList.count()).toEqual(3);
    expect(todoList.get(2).getText()).toEqual('write first protractor test');

    // You wrote your first test, cross it off the list
    todoList.get(2).element(by.css('input')).click();
    var completedAmount = element.all(by.css('.done-true'));
    expect(completedAmount.count()).toEqual(2);
  });
});

describe('GMP homepage', function() {
  it('should add a todo', function() {
    browser.get('http://127.0.0.1:8000/');
    expect(browser.getTitle()).toEqual('gmp');
    element(by.model('vm.name')).sendKeys('protractor');
    element(by.model('vm.email')).sendKeys('protractor@mail.ru');
//    var allOptions = element.all(by.model('vm.department'));
//    expect(allOptions.count()).toEqual(4);
//    var firstOption = allOptions.last();
//    expect(firstOption.getText()).toEqual('АХО');
    element.all(by.css('md-select')).each(function (eachElement, index) {
        eachElement.click(); // select the
        browser.waitForAngular(); // wait for the renderings to take effect
        element(by.css(‘md-option’)).click(); // select the first md-option
        browser.waitForAngular(); // wait for the renderings to take effect
    });
    });
  });
});
