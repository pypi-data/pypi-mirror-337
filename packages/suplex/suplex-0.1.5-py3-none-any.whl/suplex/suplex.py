import httpx
import jwt
import reflex as rx
import time

from typing import Any, Dict, List, Literal, Optional, Self
from urllib.parse import quote

class Query(rx.Base):
    """
    Query class for building and executing queries against Supabase. This class provides methods for constructing SQL-like queries.

    Init:
        - bearer_token: The JWT access token for authentication. May use access_token for query as user or service_role as admin.

    Returns:
        - httpx.Response

    Raises:
        - ValueError: If required parameters are missing or invalid.
        - httpx.HTTPStatusError: If the API request fails.
    """

    # Auth attributes
    bearer_token: str | None = None
    _api_url: str | None = None
    _api_key: str | None = None
    _headers: dict[str, str] = {}

    # Query building attributes
    _table: str | None = None
    _filters: str | None = None
    _select: str | None = None
    _order: str | None = None
    _method: str | None = None
    _data: dict[str, Any] | list | None = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        config = rx.config.get_config()
        required_keys = {"api_url", "api_key"}
        missing_keys = required_keys - config.suplex.keys() # type: ignore
        if missing_keys:
            raise ValueError(f"Missing required Suplex configuration keys: {', '.join(missing_keys)}")

        self._api_url = config.suplex["api_url"] # type: ignore
        self._api_key = config.suplex["api_key"] # type: ignore

    def table(self, table: str) -> Self:
        """Targeted table to read from."""
        self._table = f"{table}"
        return self

    def eq(self, column: str, value: Any) -> Self:
        """
        Match only rows where column is equal to value.
        https://supabase.com/docs/reference/python/eq
        """
        self._filters = f"{column}=eq.{value}"
        return self

    def neq(self, column: str, value: Any) -> Self:
        """
        Match only rows where column is not equal to value.
        https://supabase.com/docs/reference/python/neq
        """
        self._filters = f"{column}=neq.{value}"
        return self

    def gt(self, column: str, value: Any) -> Self:
        """
        Match only rows where column is greater than value.
        https://supabase.com/docs/reference/python/gt
        """
        self._filters = f"{column}=gt.{value}"
        return self

    def lt(self, column: str, value: Any) -> Self:
        """
        Match only rows where column is less than value.
        https://supabase.com/docs/reference/python/lt
        """
        self._filters = f"{column}=lt.{value}"
        return self

    def gte(self, column: str, value: Any) -> Self:
        """
        Match only rows where column is greater than or equal to value.
        https://supabase.com/docs/reference/python/gte
        """
        self._filters = f"{column}=gte.{value}"
        return self

    def lte(self, column: str, value: Any) -> Self:
        """
        Match only rows where column is less than or equal to value.
        https://supabase.com/docs/reference/python/lte
        """
        self._filters = f"{column}=lte.{value}"
        return self

    def like(self, column: str, pattern: str) -> Self:
        """
        Match only rows where column matches pattern case-sensitively.
        https://supabase.com/docs/reference/python/like
        """
        self._filters = f"{column}=like.{pattern}"
        return self

    def ilike(self, column: str, pattern: str) -> Self:
        """
        Match only rows where column matches pattern case-insensitively.
        https://supabase.com/docs/reference/python/ilike
        """
        self._filters = f"{column}=ilike.{pattern}"
        return self

    def is_(self, column: str, value: Literal["null"] | bool) -> Self:
        """
        Match only rows where column is null or bool.
        Use this instead of eq() for null values.
        https://supabase.com/docs/reference/python/is
        """
        self._filters = f"{column}=is.{value}"
        return self

    def in_(self, column: str, values: list) -> Self:
        """
        Match only rows where column is in the list of values.
        https://supabase.com/docs/reference/python/in
        """
        formatted = ",".join(quote(f'"{v}"') for v in values)
        self._filters = f"{column}=in.({formatted})"
        return self

    def contains(self, array_column: str, values: list) -> Self:
        """
        Only relevant for jsonb, array, and range columns.
        Match only rows where column contains every element appearing in values.
        https://supabase.com/docs/reference/python/contains
        """
        formatted = ",".join(quote(f'"{v}"') for v in values)
        self._filters = f"{array_column}=cs.{{{formatted}}}"
        return self

    def contained_by(self, array_column: str, values: list) -> Self:
        """
        Only relevant for jsonb, array, and range columns.
        Match only rows where every element appearing in column is contained by value.
        https://supabase.com/docs/reference/python/containedby
        """
        formatted = ",".join(quote(f'"{v}"') for v in values)
        self._filters = f"{array_column}=cd.{{{formatted}}}"
        return self

    def select(self, select: str) -> Self:
        """
        Specify columns to return, or '*' to return all.
        https://supabase.com/docs/reference/python/select
        """
        self._select = f"select={select}"
        self._method = "get"
        return self

    def insert(self, data: dict[str, Any] | list) -> Self:
        """
        Add new item to table as {'column': 'value', 'other_column': 'other_value'}
        or new items as [{'column': 'value'}, {'other_column': 'other_value'}]
        https://supabase.com/docs/reference/python/insert
        """
        self._data = data
        self._method = "post"
        return self

    def upsert(self, data: dict, return_: Literal["representation","minimal"]="representation") -> Self:
        """
        Add item to table as {'column': 'value', 'other_column': 'other_value'}
        if it doesn't exist, otherwise update item. One column must be a primary key.
        https://supabase.com/docs/reference/python/upsert
        """
        self._data = data
        self._method = "post"
        self._headers["Prefer"] = f"return={return_},resolution=merge-duplicates"
        return self

    def update(self, data: dict) -> Self:
        """
        Update lets you update rows. update will match all rows by default.
        You can update specific rows using horizontal filters, e.g. eq, lt, and is.
        https://supabase.com/docs/reference/python/update
        """
        self._headers["Prefer"] = "return=representation"
        self._method = "patch"
        self._data = data
        return self

    def delete(self) -> Self:
        """
        Delete matching rows from the table. Matches all rows by default! Use filters to specify.
        https://supabase.com/docs/reference/python/delete
        """
        self._method = "delete"
        return self

    def order(self, column: str, ascending: bool = True) -> Self:
        """
        Order the query result by column. Defaults to ascending order (lowest to highest).
        https://supabase.com/docs/reference/python/order
        """
        self._order = f"order={column}.{('asc' if ascending else 'desc')}"
        return self

    def limit(self, limit: int) -> Self:
        """
        Limit the number of rows returned.
        https://supabase.com/docs/reference/python/limit
        """
        pass
        return self

    def range(self, start: int, end: int) -> Self:
        """
        Limit the query result by starting at an offset (start) and ending at the offset (end). 
        https://supabase.com/docs/reference/python/range
        """
        pass
        return self

    def single(self) -> Self:
        """
        Return data as a single object instead of an array of objects.
        Expects a single row to be returned. If exactly one row is not returned, an error is raised.
        https://supabase.com/docs/reference/python/single
        """
        pass
        return self

    def maybe_single(self) -> Self:
        """
        Return data as a single object instead of an array of objects.
        Expects a single row to be returned. If no rows are returned, no error is raised.
        https://supabase.com/docs/reference/python/maybesingle
        """
        pass
        return self

    def csv(self) -> Self:
        """
        Return data as a string in CSV format.
        https://supabase.com/docs/reference/python/csv
        """
        pass
        return self

    def explain(self) -> Self:
        """
        For debugging slow queries, you can get the Postgres EXPLAIN execution plan
        of a query using the explain() method.
        https://supabase.com/docs/reference/python/explain
        """
        pass
        return self

    def execute(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Execute sync request to Supabase. Use async_execute() for async requests.
        Requests use httpx.Client(). See list of available parameters to pass with
        request at https://www.python-httpx.org/api/#client
        """
        # Raise exceptions
        if not self.bearer_token:
            raise ValueError("Request requires a bearer token. User needs to be signed in first, or service_role provided for admin use.")
        if not self._table:
            raise ValueError("No table name was provided for request.")
        if not self._method:
            raise ValueError("No method was provided for request.")

        # Set base URL and parameters
        base_url = f"{self._api_url}/rest/v1/{self._table}"
        params = []
        if self._filters:
            params.append(self._filters)
        if self._select:
            params.append(self._select)
        if self._order:
            params.append(self._order)
        url = f"{base_url}?{'&'.join(params)}"

        # Set headers
        headers = {
            **self._headers,
            "apikey": self._api_key,
            "Authorization": f"Bearer {self.bearer_token}",
        }

        # Finally make the built request.
        if self._method == "get":
            if not self._select:
                raise ValueError("Must select columns to return or '*' to return all.")
            response = httpx.get(url, headers=headers, **kwargs)
        elif self._method == "post":
            if not self._data:
                raise ValueError("Missing data for request.")
            response = httpx.post(url, headers=headers, json=self._data, **kwargs)
        elif self._method == "put":
            if not self._data:
                raise ValueError("Missing data for request.")
            response = httpx.put(url, headers=headers, json=self._data, **kwargs)
        elif self._method == "patch":
            if not self._data:
                raise ValueError("Missing data for request.")
            response = httpx.patch(url, headers=headers, json=self._data, **kwargs)
        elif self._method == "delete":
            response = httpx.delete(url, headers=headers, **kwargs)
        else:
            raise ValueError("Unrecognized method. Must be one of: get, post, put, patch, delete.")
        
        # Clean up
        self._table = None
        self._filters = None
        self._select = None
        self._order = None
        self._method = None
        self._data = None
        self._headers = {}
        
        # Raise any HTTP errors
        response.raise_for_status()

        # Return the response
        return response.json()

    async def async_execute(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Execute async request to Supabase. Use execute() for sync requests.
        Requests use httpx.AsyncClient(). See list of available parameters to pass with
        request at https://www.python-httpx.org/api/#asyncclient.
        """
        # Raise exceptions
        if not self.bearer_token:
            raise ValueError("Request requires a bearer token.")
        if not self._table:
            raise ValueError("No table name was provided for request.")
        if not self._method:
            raise ValueError("No method was provided for request.")

        # Set base URL and parameters
        base_url = f"{self._api_url}/rest/v1/{self._table}"
        params = []
        if self._filters:
            params.append(self._filters)
        if self._select:
            params.append(self._select)
        if self._order:
            params.append(self._order)
        url = f"{base_url}?{'&'.join(params)}"

        # Set headers
        headers = {
            **self._headers,
            "apikey": self._api_key,
            "Authorization": f"Bearer {self.bearer_token}",
        }

        async with httpx.AsyncClient() as client:
            if self._method == "get":
                if not self._table:
                    raise ValueError("No table name was provided for request.")
                if not self._select:
                    raise ValueError("Must select columns to return or '*' to return all.")
                response = await client.get(url, headers=headers, **kwargs)
            elif self._method == "post":
                if not self._data:
                    raise ValueError("Missing data for request.")
                response = await client.post(url, headers=headers, json=self._data, **kwargs)
            elif self._method == "put":
                if not self._data:
                    raise ValueError("Missing data for request.")
                response = await client.put(url, headers=headers, json=self._data, **kwargs)
            elif self._method == "patch":
                if not self._data:
                    raise ValueError("Missing data for request.")
                response = await client.patch(url, headers=headers, json=self._data, **kwargs)
            elif self._method == "delete":
                response = await client.delete(url, headers=headers, **kwargs)
            else:
                raise ValueError("Unrecognized method. Must be one of: get, post, put, patch, delete.")
            
            # Clean up
            self._table = None
            self._filters = None
            self._select = None
            self._order = None
            self._method = None
            self._data = None
            self._headers = {}
            
            # Raise any HTTP errors
            response.raise_for_status()

            # Return the response
            return response.json()


class Suplex(rx.State):
    """
    State class for managing authentication with Supabase.

    Attributes:
        - access_token - Cookie for storing the JWT access token.
        - refresh_token - Cookie for storing the refresh token.

    Vars:
        - claims: Decoded JWT claims from the access token.
        - user_id: ID of the authenticated user.
        - user_email: Email of the authenticated user.
        - user_phone: Phone number of the authenticated user.
        - user_audience: Audience of the authenticated user.
        - user_role: Role of the authenticated user.
        - claims_issuer: Issuer of the JWT claims.
        - claims_expire_at: Expiration time of the JWT claims.
        - claims_issued_at: Issued time of the JWT claims.
        - claims_session_id: Session ID from the JWT claims.
        - user_metadata: User metadata from the JWT claims.
        - app_metadata: App metadata from the JWT claims.
        - user_aal: Authentication assurance level (1 or 2).
        - user_is_authenticated: Boolean indicating if the user is authenticated.
        - user_is_anonymous: Boolean indicating if the user is anonymous.
        - user_token_expired: Boolean indicating if the token is expired.

    Auth Functions:
        - sign_up: Register a new user with email or phone and password.
        - sign_in_with_password: Authenticate a user with email/phone and password.
        - sign_in_with_oauth: Authenticate a user with third-party OAuth providers.
        - get_user: Retrieve the current authenticated user's data.
        - update_user: Update the current user's profile information.
        - refresh_session: Refresh the authentication session using the refresh token.
        - get_settings: Retrieve authentication settings for the Supabase project.
        - logout: Log out the current user and invalidate the session.

    """
    access_token: rx.Cookie | str = rx.Cookie(
        name="access_token",
        path="/",
        secure=True,
        same_site="lax",
        domain=None,
        max_age=rx.config.get_config().suplex.get("cookie_max_age", None) # type: ignore
    )
    refresh_token: rx.Cookie | str = rx.Cookie(
        name="refresh_token",
        path="/",
        secure=True,
        same_site="lax",
        domain=None,
        max_age=rx.config.get_config().suplex.get("cookie_max_age", None) # type: ignore
    )
    
    # API and auth keys
    _api_url: str | None = None
    _api_key: str | None = None
    _jwt_secret: str | None = None
    _service_role: str | None = None

    # Query class
    query: Query = Query()

    # Loading
    is_loading = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load our config
        config = rx.config.get_config()
        required_keys = {"api_url", "api_key", "jwt_secret"}
        missing_keys = required_keys - config.suplex.keys() # type: ignore
        if missing_keys:
            raise ValueError(f"Missing required Suplex configuration keys: {', '.join(missing_keys)}")

        self._api_url = config.suplex["api_url"] # type: ignore
        self._api_key = config.suplex["api_key"] # type: ignore
        self._jwt_secret = config.suplex["jwt_secret"] # type: ignore
        self._service_role = config.suplex.get("service_role", None) # type: ignore

        # Handle default cookie behavior as set by config
        default_cookie_behavior = config.suplex.get("default_cookie_behavior", "session") # type: ignore
        max_age: int | None = config.suplex.get("max_age", None) # type: ignore

    @rx.var
    def load_bearer_into_query(self) -> None:
        """
        A cheeky hack. Normally we can't access browser cookies when query is
        instantiated, but using this var we can set the access_token when the
        state has loaded prior to user interaction. Otherwise if a persistent
        cookie was set, the user would have an access_token and be "logged in"
        but not able to run queries as the bearer token would be empty.
        """
        self.query.bearer_token = self.access_token

    @rx.var
    def claims(self) -> Dict[str, Any] | None:
        if self.access_token:
            try:
                claims = jwt.decode(
                    self.access_token,
                    self._jwt_secret, # type: ignore
                    algorithms=["HS256"],
                    audience="authenticated",
                )
                return claims
            except Exception:
                return None
            
    @rx.var
    def user_id(self) -> str | None:
        if self.claims:
            return self.claims["sub"]
        return None
    
    @rx.var
    def user_email(self) -> str | None:
        if self.claims:
            return self.claims["email"]
        return None
    
    @rx.var
    def user_phone(self) -> str | None:
        if self.claims:
            return self.claims["phone"]
        return None
    
    @rx.var
    def user_audience(self) -> str | None:
        if self.claims:
            return self.claims["aud"]
        return None
    
    @rx.var
    def user_role(self) -> str | None:
        if self.claims:
            return self.claims["role"]
        return None
    
    @rx.var
    def claims_issuer(self) -> str | None:
        if self.claims:
            return self.claims["iss"]
        return None
    
    @rx.var
    def claims_expire_at(self) -> int | None:
        """Unix timestamp of when the token expires."""
        if self.claims:
            return self.claims["exp"]
        return None
    
    @rx.var
    def claims_issued_at(self) -> int | None:
        """Unix timestamp of when the token was issued."""
        if self.claims:
            return self.claims["iat"]
        return None
    
    @rx.var
    def claims_session_id(self) -> str | None:
        """Unique identifier for the session."""
        if self.claims:
            return self.claims["session_id"]
        return None
    
    @rx.var
    def user_metadata(self) -> Dict[str, Any] | None:
        if self.claims:
            return self.claims["user_metadata"]
        return None
    
    @rx.var
    def app_metadata(self) -> Dict[str, Any] | None:
        if self.claims:
            return self.claims["app_metadata"]
        return None
    
    @rx.var
    def user_aal(self) -> Literal["aal1", "aal2"] | None:
        """aal1 is 1-factor auth, aal2 is 2-factor auth."""
        if self.claims:
            return self.claims["aal"]
        return None
            
    @rx.var
    def user_is_authenticated(self) -> bool:
        if self.claims:
            return True if self.claims["aud"] == "authenticated" else False
        return False
    
    @rx.var
    def user_is_anonymous(self) -> bool:
        if self.claims:
            return self.claims["is_anonymous"]
        return False
    
    @rx.var
    def user_token_expired(self) -> bool:
        """Give 10 seconds of leeway for token expiration for a slow request."""
        if self.claims:
            return True if self.claims_expire_at + 10 < time.time() else False
        return False
        
    def sign_up(
        self,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        password: str = "",
        options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Register a new user with email or phone and password.
        
        Args:
            email: The email address of the user. Either email or phone must be provided.
            phone: The phone number of the user. Either email or phone must be provided.
            password: The password for the user (required).
            options: Additional options for the signup process:
                - email_redirect_to: URL to redirect after email confirmation
                - data: Custom user metadata to store
                - captcha_token: Token from a captcha provider
                - channel: Channel for sending messages (phone signups only)
                
        Returns:
            Dict containing the user data and authentication tokens.
            
        Raises:
            ValueError: If neither email nor phone is provided, or if password is missing.
            httpx.HTTPStatusError: If the API request fails.
        """
        data = {}
        url = f"{self._api_url}/auth/v1/signup"
        headers = {
            "apikey": self._api_key,
        }
        if not email and not phone:
            raise ValueError("Either email or phone must be provided.")
        if not password:
            raise ValueError("Password must be provided.")

        data["password"] = password
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if options:
            if "data" in options:
                data["data"] = options.pop("data")
            if "email_redirect_to" in options:
                data["email_redirect_to"] = options.pop("email_redirect_to")
            if "captcha_token" in options:
                data["captcha_token"] = options.pop("captcha_token")
            if "channel" in options:
                data["channel"] = options.pop("channel")

        response = httpx.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()

    def sign_in_with_password(
        self,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        password: str = "",
        options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Authenticate a user with email/phone and password.
        
        Args:
            email: The email address of the user. Either email or phone must be provided.
            phone: The phone number of the user. Either email or phone must be provided.
            password: The password for authentication (required).
            options: Additional options for the signin process:
                - captcha_token: Token from a captcha provider
                
        Returns:
            Dict containing user data, access_token, refresh_token, and other session info.
            
        Raises:
            ValueError: If neither email nor phone is provided, or if password is missing.
            httpx.HTTPStatusError: If the API request fails (e.g., invalid credentials).
        """
        data = {}
        url = f"{self._api_url}/auth/v1/token?grant_type=password"
        headers = {
            "apikey": self._api_key,
        }

        data["password"] = password
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if options:
            if "captcha_token" in options:
                data["captcha_token"] = options.pop("captcha_token")

        response = httpx.post(url, headers=headers, json=data)
        response.raise_for_status()

        response_data = response.json()

        self.access_token = response_data["access_token"]
        self.query.bearer_token = response_data["access_token"]
        self.refresh_token = response_data["refresh_token"]

        return response_data

    def sign_in_with_oauth(
        self,
        provider: Literal[
            "google",
            "facebook",
            "apple",
            "azure",
            "twitter",
            "github",
            "gitlab",
            "bitbucket",
            "discord",
            "figma",
            "kakao",
            "keycloak",
            "linkedin_oidc",
            "notion",
            "slack_oidc",
            "spotify",
            "twitch",
            "workos",
            "zoom",
        ],
        options: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate a URL for OAuth authentication with a third-party provider.
        
        Args:
            provider: The OAuth provider to use (must be one of the supported providers).
            options: Additional options for the OAuth flow:
                - redirect_to: URL to redirect after authentication
                - scopes: List of permission scopes to request
                - query_params: Additional parameters to include in the OAuth request
                
        Returns:
            A URL string to redirect the user to for OAuth authentication.
            
        Raises:
            ValueError: If the provider is not supported.
            httpx.HTTPStatusError: If the API request fails.
            
        Note:
            The returned URL should be used with rx.redirect() to redirect
            the user to the OAuth provider's login page.
        """
        data = {}
        url = f"{self._api_url}/auth/v1/authorize"
        data["provider"] = provider
        if options:
            if "redirect_to" in options:
                data["redirect_to"] = options.pop("redirect_to")
            if "scopes" in options:
                data["scopes"] = options.pop("scopes")
            if "query_params" in options:
                data["query_params"] = options.pop("query_params")

        response = httpx.get(url, headers=self._headers, params=data)

        if response.status_code == 302:
            return response.headers["location"]
        
        # If not a redirect response, check for other errors
        response.raise_for_status()
        raise ValueError("Expected a redirect response from OAuth provider, but none was received.")

    def get_user(self) -> Optional[Dict[str, Any]]:
        """
        Retrieve the current authenticated user's data from the database.
        
        This method gets the current user information from the Supabase API.
        It first verifies that the session is valid, and if not, returns None.
        
        Args:
            None
            
        Returns:
            A dictionary containing the user data if authenticated, or None if:
            - No valid session exists
            - The access token is expired and refresh fails
            - Any error occurs during API request
            
        Note:
            This method will clear auth tokens if an error occurs.
            Use get_session() to retrieve the JWT token claims instead of the full user profile.
        """
        response = httpx.get(
            f"{self._api_url}/auth/v1/user",
            headers={
                "apikey": self._api_key,
                "Authorization": f"Bearer {self.access_token}",
            },
        )
        response.raise_for_status()
        return response.json()

    def update_user(
        self,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        password: Optional[str] = None,
        user_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Update the current user's profile information.
        
        This method updates one or more user attributes including email,
        phone number, password, or custom metadata.
        
        Args:
            email: New email address for the user
            phone: New phone number for the user
            password: New password for the user
            user_metadata: Dictionary of custom metadata to store with the user profile
            
        Returns:
            Dictionary containing the updated user data
            
        Raises:
            ValueError: If no access token exists (user not authenticated)
            httpx.HTTPStatusError: If the API request fails
        """
        if not self.access_token:
            raise ValueError("Expected access token to update user information.")

        data = {}
        url = f"{self._api_url}/auth/v1/user"
        headers = {
            "apikey": self._api_key,
            "Authorization": f"Bearer {self.access_token}",
        }

        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if password:
            data["password"] = password
        if user_metadata:
            data["data"] = user_metadata
            
        if not data:
            raise ValueError("At least one attribute (email, phone, password, or user_metadata) must be provided to update.")

        response = httpx.put(url, headers=headers, json=data)
        response.raise_for_status()

        return response.json()

    def refresh_session(self) -> Dict[str, Any] | None:
        """
        Refresh the authentication session using the refresh token.
        
        This method uses the stored refresh token to obtain a new access token
        when the current one expires. It automatically updates the token storage
        if successful.
        
        Returns:
            - Dictionary containing the user data if refresh successful.
            - None if:
                - No refresh token exists
                - Refresh token is expired or invalid
                - API request fails for any reason

        Raises:
            httpx.HTTPStatusError: If the API request fails
            KeyError: If the expected keys are not present in the response
        """
        url = f"{self._api_url}/auth/v1/token?grant_type=refresh_token"
        headers = {
            "apikey": self._api_key,
            "Authorization": f"Bearer {self.access_token}",
        }
        response = httpx.post(
            url, 
            headers=headers, 
            json={"refresh_token": self.refresh_token}
        )
        response.raise_for_status()

        self.access_token = response.json()["access_token"]
        self.refresh_token = response.json()["refresh_token"]
        return response.json()["user"]

    def get_settings(self) -> Dict[str, Any]:
        """
        Retrieve the authentication settings for the Supabase project.
        
        This method fetches the authentication configuration settings from
        the Supabase API, including enabled providers and security settings.
            
        Returns:
            Dictionary containing the authentication settings
            
        Raises:
            httpx.HTTPStatusError: If the API request fails
        """
        url = f"{self._api_url}/auth/v1/settings"
        headers = {
            "apikey": self._api_key,
        }
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def log_out(self) -> None:
        """
        Log out the current user and invalidate the refresh token on Supabase.
        Clears cookies and the bearer token from the query object.
            
        Raises:
            httpx.HTTPStatusError: If the API request fails.
        """
        # Only attempt server-side logout if we have an access token
        if self.access_token:
            url = f"{self._api_url}/auth/v1/logout"
            headers = {
                "apikey": self._api_key,
                "Authorization": f"Bearer {self.access_token}",
            }
            response = httpx.post(url, headers=headers)

            # Clear tokens
            self.access_token = ""
            self.refresh_token = ""
            self.query.bearer_token = ""

            # Up to dev how to handle if server exception occurs, but locally user will be logged out.
            response.raise_for_status()

        else:
            # Clear tokens if no access token exists
            self.access_token = ""
            self.refresh_token = ""
            self.query.bearer_token = ""