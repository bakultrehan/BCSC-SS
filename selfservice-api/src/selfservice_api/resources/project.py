# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""API endpoints for managing project resource."""

from http import HTTPStatus

from flask import current_app, g, jsonify, request
from flask_restplus import Namespace, Resource, cors
from marshmallow import ValidationError

from ..models import OIDCConfig, Project, TechnicalReq, TestAccount, User
from ..models.enums import ProjectRoles, ProjectStatus
from ..schemas.project import ProjectSchema
from ..services.external import get_dynamic_api
from ..services.external.models import CreateRequestModel, CreateResponseModel, UpdateRequestModel, UpdateResponseModel
from ..services.notification import EmailService, EmailType
from ..utils.auth import auth
from ..utils.roles import Role
from ..utils.util import cors_preflight


API = Namespace('Project', description='Project')


@cors_preflight('GET,POST,OPTIONS')
@API.route('', methods=['GET', 'POST', 'OPTIONS'])
class ProjectResource(Resource):
    """Resource for managing create project."""

    @staticmethod
    @cors.crossdomain(origin='*')
    @auth.has_one_of_roles([Role.ss_client, Role.ss_admin])
    def get():
        """Get all project."""
        token_info = g.jwt_oidc_token_info
        oauth_id = None
        if auth.is_client_role():
            oauth_id = token_info.get('sub')
        projects = Project.find_all_or_by_user(oauth_id)
        return jsonify({'projects': projects}), HTTPStatus.OK

    @staticmethod
    @cors.crossdomain(origin='*')
    @auth.require
    def post():
        """Post a new project using the request body."""
        project_json = request.get_json()

        try:
            token_info = g.jwt_oidc_token_info
            project_schema = ProjectSchema()
            dict_data = project_schema.load(project_json)
            project = Project.create_from_dict(dict_data, token_info.get('sub'))
            response, status = project_schema.dump(project), HTTPStatus.CREATED
        except ValidationError as project_err:
            response, status = {'message': str(project_err.messages)}, \
                HTTPStatus.BAD_REQUEST
        return response, status


@cors_preflight('GET,PUT,PATCH,OPTIONS')
@API.route('/<int:project_id>', methods=['GET', 'PUT', 'PATCH', 'OPTIONS'])
class ProjectResourceById(Resource):
    """Resource for managing get project by id."""

    @staticmethod
    @cors.crossdomain(origin='*')
    @auth.can_access_project([ProjectRoles.Developer, ProjectRoles.Manager, ProjectRoles.Cto])
    def get(project_id):
        """Get project details."""
        token_info = g.jwt_oidc_token_info
        user = User.find_by_oauth_id(token_info.get('sub'))
        project = Project.find_by_id(project_id)
        project_dump = ProjectSchema().dump(project)
        for project_users in project.users:
            if project_users.user_id == user.id:
                project_dump['myRole'] = project_users.role
        return project_dump, HTTPStatus.OK

    @staticmethod
    @cors.crossdomain(origin='*')
    @auth.can_access_project([ProjectRoles.Developer, ProjectRoles.Manager, ProjectRoles.Cto])
    def put(project_id):
        """Update project details."""
        project_json = request.get_json()

        try:
            project_schema = ProjectSchema()
            dict_data = project_schema.load(project_json)

            project = Project.find_by_id(project_id)
            token_info = g.jwt_oidc_token_info
            project.update(token_info.get('sub'), dict_data)
            return 'Updated successfully', HTTPStatus.OK
        except ValidationError as project_err:
            return {'message': str(project_err.messages)}, HTTPStatus.BAD_REQUEST

    @staticmethod
    @cors.crossdomain(origin='*')
    @auth.can_access_project([ProjectRoles.Developer, ProjectRoles.Manager, ProjectRoles.Cto])
    def patch(project_id):
        """Update project status."""
        project_patch_json = request.get_json()

        project = Project.find_by_id(project_id)
        if 'update' in project_patch_json:
            if project_patch_json['update'] == 'status' and \
                    ProjectResourceById._validate_before_status_update_(project, project_patch_json.get('status')):

                project_status = project_patch_json['status']
                is_success = False
                # Decide which api to call
                if project_status == ProjectStatus.Development:
                    is_success = ProjectResourceById._dynamic_api_call_(project, False)
                    if is_success:
                        response = ProjectResourceById._update_development_status_(project, project_status)

                if is_success:
                    status = HTTPStatus.OK
                else:
                    response, status = 'OIDC Failed', HTTPStatus.INTERNAL_SERVER_ERROR
                return response, status

        return 'Update failed', HTTPStatus.BAD_REQUEST

    @staticmethod
    def _update_development_status_(project: Project, status):
        """Update project status to development."""
        token_info = g.jwt_oidc_token_info
        EmailService.save_and_send(EmailType.DEV_REQUEST, {'project_name': project.project_name})

        # Make sure we are not downgrading the project status
        if project.status < status:
            project.update_status(token_info.get('sub'), status)

        test_accounts = TestAccount.find_all_by_project_id(project.id)
        technical_req: TechnicalReq = project.technical_req[0]
        response = {
            'testAccountSuccess': True,
            'message': 'Updated successfully'
        }
        if len(test_accounts) < technical_req.no_of_test_account:
            response['testAccountSuccess'] = False

        return response

    @staticmethod
    def _validate_before_status_update_(project: Project, status):
        """Validate the project details before updating status."""
        if project is not None:
            if status == ProjectStatus.Development:
                technical_req = TechnicalReq.find_by_project_id(project.id)
                if technical_req is not None and \
                    technical_req.scope_package_id is not None and \
                        technical_req.no_of_test_account is not None:
                    return True

        return False

    @staticmethod
    def _dynamic_api_call_(project: Project, is_prod: bool):
        """Generate OIDC config for this project."""
        api_call_succeeded = True
        dynamic_api = get_dynamic_api()

        oidc_config = OIDCConfig.find_by_project_id(project.id)
        api_request = ProjectResourceById._generate_api_request_(project, is_prod, oidc_config)

        if oidc_config is None:
            api_response: CreateResponseModel = dynamic_api.create(api_request)

            if api_response is not None:
                OIDCConfig.create_from_dict(
                    ProjectResourceById._map_response_to_oidc_config_(False, project, api_response))
            else:
                api_call_succeeded = False
        else:
            api_request.client_id = oidc_config.client_id
            api_response: UpdateResponseModel = \
                dynamic_api.update(oidc_config.registration_access_token, api_request)

            if api_response is not None:
                oidc_config.update(
                    ProjectResourceById._map_response_to_oidc_config_(True, project, api_response))
            else:
                api_call_succeeded = False

        if not is_prod and api_call_succeeded:
            technical_req: TechnicalReq = project.technical_req[0]
            TestAccount.map_test_accounts(project.id, technical_req.no_of_test_account)
            trigger_count = current_app.config.get('LIMITED_TEST_ACCOUNT_TRIGGER_COUNT')
            if TestAccount.get_availability_count() <= trigger_count:

                EmailService.save_and_send(EmailType.TEST_ACCOUNT, {})

        return api_call_succeeded

    @staticmethod
    def _generate_api_request_(project: Project, is_prod: bool, oidc_config: OIDCConfig):
        """Create dynaamic api request object."""
        if oidc_config is None:
            api_request = CreateRequestModel()
        else:
            api_request = UpdateRequestModel()

        api_request.client_name = project.project_name
        api_request.contacts = []
        for user_association in project.users:
            api_request.contacts.append(user_association.user.email)

        technical_req: TechnicalReq = project.technical_req[0]
        api_request.client_uri = technical_req.client_uri
        api_request.redirect_uris = technical_req.redirect_uris
        api_request.scope = technical_req.scope_package.scope
        api_request.jwks_uri = technical_req.jwks_uri
        api_request.id_token_signed_response_alg = technical_req.id_token_signed_response_alg
        api_request.userinfo_signed_response_alg = technical_req.userinfo_signed_response_alg
        api_request.token_endpoint_auth_method = None
        api_request.id_token_encrypted_response_alg = technical_req.id_token_encrypted_response_alg
        api_request.id_token_encrypted_response_enc = None
        api_request.userinfo_encrypted_response_alg = technical_req.userinfo_encrypted_response_alg
        api_request.userinfo_encrypted_response_enc = None

        if is_prod:
            api_request.api_url = current_app.config.get('DYNAMIC_PROD_API_URL')
            api_request.api_token = current_app.config.get('DYNAMIC_PROD_API_TOKEN')
        else:
            api_request.api_url = current_app.config.get('DYNAMIC_TEST_API_URL')
            api_request.api_token = current_app.config.get('DYNAMIC_TEST_API_TOKEN')

        return api_request

    @staticmethod
    def _map_response_to_oidc_config_(is_update: bool, project, api_response):
        """Map response to OIDC config."""
        data = {
            'project_id': project.id,
            'client_id': api_response.client_id,
            'client_secret': api_response.client_secret,
            'registration_access_token': api_response.registration_access_token,
            'registration_client_uri': api_response.registration_client_uri,
            'client_id_issued_at': api_response.client_id_issued_at,
            'client_secret_expires_at': api_response.client_secret_expires_at,
            'token_endpoint_auth_method': api_response.token_endpoint_auth_method
        }

        if not is_update:
            data['application_type'] = api_response.application_type
            data['subject_type'] = api_response.subject_type

        return data
