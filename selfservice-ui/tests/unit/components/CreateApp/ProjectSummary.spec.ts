import { shallowMount, mount } from '@vue/test-utils';
import ProjectSummary from '@/components/CreateApp/ProjectSummary.vue';
import Vuetify from 'vuetify';
import Vuex from 'vuex';
import { singleProject } from '../../mocks/projectinfo';
let vuetify: any;
vuetify = new Vuetify();

const technicalReq = {
  clientUri: 'app.com',
  id: 15,
  encryptedResponseAlg: 'RS256',
  jwksUri: 'jwks2.com',
  noOfTestAccount: 3,
  noteTestAccount: '',
  projectId: 12,
  redirectUris: ['test.com'],
  scopePackageId: 3,
  signedResponseAlg: 'RS256',
};

describe('ProjectSummary.vue', () => {
  const store = new Vuex.Store({
    modules: {
      ProjectInfoModule: {
        namespaced: true,
        state: {},
        getters: {
          getSingleProjectInfo: jest.fn(() => {
            return {
              singleProject,
            };
          }),
          getFinalProjectSubmissionStatus: jest.fn(),
          errorStatus: jest.fn(),
        },
        actions: {
          loadSingleProjectInfo: jest.fn(),
        },
      },
      TeamRolesModule: {
        namespaced: true,
        state: {},
        getters: {
          getTeamList: jest.fn(() => {
            return {
              team: [
                {
                  email: 'e@e.com',
                  firstName: 'fname',
                  id: 1,
                  lastName: 'lname',
                  phone: '09870987654321',
                  role: 2,
                },
                {
                  email: 'bb@test.com',
                  firstName: 'john',
                  id: 17,
                  lastName: 'bb',
                  phone: '987654321',
                  role: 3,
                },
                {
                  email: 'user@yopmail.com',
                  firstName: 'John',
                  id: 1,
                  lastName: 'Doe',
                  phone: '',
                  role: 1,
                },
              ],
            };
          }),
        },
        actions: {
          loadTeam: jest.fn(),
        },
      },
      TechnicalReqModule: {
        namespaced: true,
        state: {},
        getters: {
          getTechnicalReq: jest.fn(() => {
            return technicalReq;
          }),
          errorStatus: jest.fn(),
        },
        actions: {
          loadTechnicalReqDetails: jest.fn(),
        },
      },
      PackageAndTestModule: {
        namespaced: true,
        state: {},
        getters: {
          successStatus: jest.fn(),
          getPackageList: jest.fn(() => {
            return [
              {
                claimNames: ['Given name', 'Surname'],
                description: 'This package contains the following data:',
                id: 1,
                packageName: 'Package 1',
              },
            ];
          }),
        },
        actions: {
          loadPackage: jest.fn(),
        },
      },
      SharedModule: {
        namespaced: true,
        state: {},
        getters: {
          isRedirectFromSummaryPage: jest.fn(),
        },
        actions: {
          redirectFromSummaryPage: jest.fn(),
        },
      },
      ClientIdModule: {
        namespaced: true,
        state: {},
        getters: {
          isLoading: jest.fn(),
          getApiData: jest.fn(() => {
            return {
              oidcConfig: {
                clientId: 'new client',
                clientSecret: 'new secret',
              },
              testUserAccounts: [
                {
                  userName: 'iuser1',
                  idKey: 'my key',
                },
              ],
            };
          }),
          errorStatus: jest.fn(),
        },
        actions: {
          getClientIdDetails: jest.fn(),
        },
      },
    },
  });

  const mountFunction = (options: any) => {
    return mount(ProjectSummary, {
      store,
      vuetify,
      mocks: { $t: jest.fn(() => {}) }, // tslint:disable-line
      ...options,
    });
  };

  it('renders props when passed with gettors', () => {
    const projectSummary = mountFunction({});

    expect(projectSummary.element).toMatchSnapshot();
  });

  it('show modal on click', () => {
    const projectSummary = mountFunction({});

    projectSummary.setData({ isLoading: false });
    const button = projectSummary.find('.submit-package');
    projectSummary.vm.$on('action-btn:clicked', jest.fn());
    button.trigger('click');
    expect(projectSummary.element).toMatchSnapshot();
  });
});

describe('ProjectSummary.vue', () => {
  it('renders props when passed', () => {
    const store = new Vuex.Store({
      modules: {
        ProjectInfoModule: {
          namespaced: true,
          state: {},
          getters: {
            getSingleProjectInfo: jest.fn(),
            errorStatus: jest.fn(),
            getFinalProjectSubmissionStatus: jest.fn(),
          },
          actions: {
            loadSingleProjectInfo: jest.fn(),
          },
        },
        TeamRolesModule: {
          namespaced: true,
          state: {},
          getters: {
            getTeamList: jest.fn(),
          },
          actions: {
            loadTeam: jest.fn(),
          },
        },
        TechnicalReqModule: {
          namespaced: true,
          state: {},
          getters: {
            getTechnicalReq: jest.fn(() => {
              return technicalReq;
            }),
            errorStatus: jest.fn(),
          },
          actions: {
            loadTechnicalReqDetails: jest.fn(),
          },
        },
        PackageAndTestModule: {
          namespaced: true,
          state: {},
          getters: {
            successStatus: jest.fn(),
            getPackageList: jest.fn(),
          },
          actions: {
            loadPackage: jest.fn(),
          },
        },
        SharedModule: {
          namespaced: true,
          state: {},
          getters: {
            isRedirectFromSummaryPage: jest.fn(),
          },
          actions: {
            redirectFromSummaryPage: jest.fn(),
          },
        },
      },
    });
    const projectSummary = shallowMount(ProjectSummary, {
      vuetify,
      store,
      mocks: { $t: jest.fn(() => {}) }, // tslint:disable-line
    });

    expect(projectSummary.element).toMatchSnapshot();
  });
});
