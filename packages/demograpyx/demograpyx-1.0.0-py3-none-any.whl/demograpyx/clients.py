from types import TracebackType
from typing import Any, Optional, Sequence
from urllib.parse import urlencode

import aiohttp
import warnings

from demograpyx.exceptions import ApiKeyWarning, HTTPError
from demograpyx.objects import AgePrediction, CountryPrediction, GenderPrediction, NationalityPrediction, Prediction

__all__ = ("Predictor", "Genderize", "Agify", "Nationalize")

class Predictor:
    """Base client class for Demografix's APIs. Serves as a framework for Genderize, Agify and Nationalize predictors.
    """
    URL: str = ""

    @classmethod
    async def create(cls, api_key: Optional[str] = None) -> "Predictor":
        """Create a predictor object with its own aiohttp session

        Args:
            api_key (str, optional): API key to pass to requests, required for more than 100 requests per day. Defaults to None.

        Returns:
            Predictor: A new predictor object.
        """
        return cls(api_key=api_key, session=aiohttp.ClientSession())

    def __init__(self, *, session: aiohttp.ClientSession, api_key: Optional[str] = None) -> None:
        """Initialise a predictor object

        Args:
            api_key (str, optional): API key to pass to requests, required for more than 100 requests per day. Defaults to None.
            session (aiohttp.ClientSession): aiohttp session to be used, which must be initilaised in an async function.
        """
        self.api_key = api_key
        self.session = session
        if self.api_key is None:
            warnings.warn("No API key passed. Demografix's APIs are free for up to 100 names per day without a key, please sign up for more requests.", ApiKeyWarning)

    async def __aenter__(self) -> "Predictor":
        """Context manager ("async with" statement) entry point. Initialises an aiohttp session if one is not present."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type: type[BaseException], exc_value: Optional[BaseException], exc_traceback: Optional[TracebackType]) -> None:
        """Context manager ("async with" statement) exit point. Closes the predictor's aiohttp session."""
        if self.session is not None:
            await self.session.close()

    async def _request(self, params: dict[str, Any]) -> dict[str, Any]:
        """Sends a HTTP request to the URL defined in the `URL` classvar

        Args:
            params (dict[str, Any]): Parameters to be passed to the request as queries.

        Raises:
            HTTPError: HTTP error message with accompanying status code attribute.

        Returns:
            dict[str, Any]: The response in JSON format.
        """
        request_url = self.URL + "?" + urlencode(params, doseq=True)
        async with self.session.get(request_url) as request:
            res = await request.json()
            if "error" in res:
                raise HTTPError(res["error"], code=request.status)
            return res
        
    async def close(self) -> None:
        """Close the predictor's HTTP session"""
        await self.session.close()

    async def predict(self, name: str, country_id: Optional[str] = None) -> Prediction:
        """Predict data for a name. This function is to be implemented in a subclass

        Args:
            name (str): The name to predict based on. 
            country_id (str, optional): ISO 3166-1 alpha-2 country code, can improve prediction accuracy. Defaults to None.

        Returns:
            Prediction: A prediction object containing data for the name given.
        """
        return NotImplemented
    
    async def batch_predict(self, names: Sequence[str], country_id: Optional[str] = None) -> list[Prediction]:
        """Predict data for a list of names. This function is to be implemented in a subclass

        Args:
            names (Sequence[str]): A sequence of names
            country_id (str, optional): ISO 3166-1 alpha-2 country code, can improve prediction accuracy. Applies to all names in the list. Defaults to None.

        Returns:
            list[Prediction]: A list of prediction objects containing data for each name
        """
        return NotImplemented

class Genderize(Predictor):
    """Predictor class for the Genderize API."""

    URL = "https://api.genderize.io/"

    async def predict(self, name: str, country_id: Optional[str] = None) -> GenderPrediction:
        """Predict a person's gender

        Args:
            name (str): The name of the person
            country_id (str, optional): ISO 3166-1 alpha-2 country code, can improve prediction accuracy. Defaults to None.

        Returns:
            GenderPrediction: A prediction of the person's gender
        """
        request_params = {"name": name}
        if country_id is not None:
            request_params["country_id"] = country_id
        if self.api_key is not None:
            request_params["apikey"] = self.api_key

        res = await self._request(request_params)
            
        return GenderPrediction(**res)
    
    async def batch_predict(self, names: Sequence[str], country_id: Optional[str] = None) -> list[GenderPrediction]:
        """Predict genders for a list of names

        Args:
            names (Sequence[str]): The list of names to be provided
            country_id (str, optional): ISO 3166-1 alpha-2 country code, can improve prediction accuracy. Applies to all names in the list. Defaults to None.

        Returns:
            list[GenderPrediction]: A list of gender predictions for each name
        """
        request_params = {"name[]": names}
        if country_id is not None:
            request_params["country_id"] = country_id
        if self.api_key is not None:
            request_params["apikey"] = self.api_key

        res = await self._request(request_params)
            
        return [GenderPrediction(**prediction) for prediction in res]
    
class Agify(Predictor):
    """Predictor class for the Agify API."""

    URL = "https://api.agify.io/"

    async def predict(self, name: str, country_id: Optional[str] = None) -> AgePrediction:
        """Predict a person's age

        Args:
            name (str): The name of the person
            country_id (str, optional): ISO 3166-1 alpha-2 country code, can improve prediction accuracy. Defaults to None.

        Returns:
            AgePrediction: A prediction of the person's age
        """
        request_params = {"name": name}
        if country_id is not None:
            request_params["country_id"] = country_id
        if self.api_key is not None:
            request_params["apikey"] = self.api_key

        res = await self._request(request_params)
            
        return AgePrediction(**res)
    
    async def batch_predict(self, names: Sequence[str], country_id: Optional[str] = None) -> list[AgePrediction]:
        """Predict ages for a list of names

        Args:
            names (Sequence[str]): The list of names to be provided
            country_id (str, optional): ISO 3166-1 alpha-2 country code, can improve prediction accuracy. Applies to all names in the list. Defaults to None.

        Returns:
            list[AgePrediction]: A list of age predictions for each name
        """
        request_params = {"name[]": names}
        if country_id is not None:
            request_params["country_id"] = country_id
        if self.api_key is not None:
            request_params["apikey"] = self.api_key

        res = await self._request(request_params)
            
        return [AgePrediction(**prediction) for prediction in res]
    
class Nationalize(Predictor):
    """Predictor class for the Nationalize API."""

    URL = "https://api.nationalize.io/"

    async def predict(self, name: str) -> NationalityPrediction:
        """Predict a person's nationality

        Args:
            name (str): The name of the person

        Returns:
            NationalityPrediction: A prediction of the input name's nationality
        """
        request_params = {"name": name}
        if self.api_key is not None:
            request_params["apikey"] = self.api_key

        res = await self._request(request_params)
            
        return NationalityPrediction(count=res["count"], name=res["name"], countries=[CountryPrediction(**country) for country in res["country"]])
    
    async def batch_predict(self, names: Sequence[str]) -> list[NationalityPrediction]:
        """Predict nationalities for a list of names

        Args:
            names (Sequence[str]): The list of names to be provided

        Returns:
            list[NationalityPrediction]: A list of nationality predictions for each name
        """
        request_params = {"name[]": names}
        if self.api_key is not None:
            request_params["apikey"] = self.api_key

        res = await self._request(request_params)
            
        return [NationalityPrediction(count=prediction["count"], name=prediction["name"], countries=[CountryPrediction(**country) for country in prediction["country"]]) for prediction in res]