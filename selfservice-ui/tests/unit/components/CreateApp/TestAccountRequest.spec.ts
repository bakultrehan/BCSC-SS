import { mount, createLocalVue } from '@vue/test-utils';
import TestAccountRequest from '@/components/CreateApp/TestAccountRequest.vue';
import Vuetify from 'vuetify';
import Vuex from 'vuex';

describe('TestAccountRequest.vue', () => {
  let vuetify: any;
  const localVue = createLocalVue();

  const $t = localVue.use(Vuetify);
  localVue.use(Vuex);
  vuetify = new Vuetify();
  const store = new Vuex.Store({
    modules: {
      PackageAndTestModule: {
        namespaced: true,
        state: {},
        getters: {
          isLoggedin: jest.fn(),
          successStatus: jest.fn(),
          errorStatus: jest.fn()
        },
        actions: {
          addTestAccountRequestToProject: jest.fn()
        }
      },
      TechnicalReqModule: {
        namespaced: true,
        state: {},
        getters: {
          getSingleTechnicalReq: jest.fn(),
          getTechnicalReq: jest.fn(),
          isLoading: jest.fn()
        },
        actions: {
          getSingleTechnicalReq: jest.fn(),
          addTechnicalReq: jest.fn()
        }
      },
      SharedModule: {
        namespaced: true,
        state: {},
        getters: {
          isRedirectFromSummaryPage: jest.fn(() => {
            return false;
          })
        },
        actions: {
          redirectFromSummaryPage: jest.fn()
        }
      }
    }
  });

  const mountFunction = (options: any) => {
    return mount(TestAccountRequest, {
      store,
      vuetify,
      localVue,
      mocks: { $t: jest.fn(() => {}) }, // tslint:disable-line
      ...options
    });
  };

  it('renders props when passed', () => {
    const TestReqWrapper = mountFunction({});

    expect(TestReqWrapper.element).toMatchSnapshot();
  });

  it('select on package on click ', () => {
    const TestReqWrapper = mountFunction({});
    const event = jest.fn();
    const button = TestReqWrapper.find('.test-account');
    TestReqWrapper.vm.$on('action-btn:clicked', event);
    button.trigger('click');

    expect(TestReqWrapper.element).toMatchSnapshot();
  });

  it('submit form with selected package on submit click ', () => {
    const TestReqWrapper = mountFunction({});
    const event = jest.fn();
    const button = TestReqWrapper.find('.submit-account');
    TestReqWrapper.vm.$on('action-btn:clicked', event);
    button.trigger('click');

    expect(TestReqWrapper.element).toMatchSnapshot();
  });
});
