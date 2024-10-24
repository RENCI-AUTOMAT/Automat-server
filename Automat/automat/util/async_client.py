import aiohttp
import traceback
import json
from automat.config import config
from automat.util.logutil import LoggingUtil


logger = LoggingUtil.init_logging(__name__,
                                  config.get('logging_level'),
                                  config.get('logging_format')
                                  )


async def async_get_json(url, headers=None, timeout=5*6):
    """
        Gets json response from url asyncronously.
    """
    client_timeout = aiohttp.ClientTimeout(connect=timeout)
    async with aiohttp.ClientSession(timeout=client_timeout) as session:
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    # here we use text() instead of json() because we trust it's proper json
                    # there's no need to unpack and repack it
                    return await response.text(), 200
                else:
                    error = f"Plater {url} returned an unsuccessful status code ({response.status})."
                    logger.error(error)
                    return json.dumps({'error': error,
                                       'code': response.status,
                                       'response': await response.text()}), response.status
        except aiohttp.ClientError as e:
            logger.error(f"Error contacting {url} -- {e}")
            logger.info(traceback.print_exc())
            return json.dumps({"error": f"An error occurred while calling the server at {url} ({e})"}), 500
        except Exception as e:
            error_message = f"An error occurred in Automat while calling {url} ({e})."
            logger.error(error_message)
            logger.info(traceback.print_exc())
            return json.dumps({"error": error_message}), 500


async def async_post_json(url, headers=None, body='', timeout=5*6):
    client_timeout = aiohttp.ClientTimeout(connect=timeout)
    async with aiohttp.ClientSession(timeout=client_timeout) as session:
        try:
            async with session.post(url, data=body, headers=headers) as response:
                if response.status == 200:
                    # here we use text() instead of json() because we trust it's proper json
                    # there's no need to unpack and repack it
                    return await response.text(), 200
                else:
                    error = f"Plater {url} returned an unsuccessful status code ({response.status})."
                    logger.error(error)
                    return json.dumps({'error': error,
                                       'code': response.status,
                                       'response': await response.text()}), response.status
        except aiohttp.ClientError as e:
            logger.error(f"Error contacting {url} -- {e}")
            logger.info(traceback.print_exc())
            return json.dumps({"error": f"An error occurred while calling the server at {url} ({e})"}), 500
        except Exception as e:
            error_message = f"An error occurred in Automat while calling {url} ({e})."
            logger.error(error_message)
            logger.info(traceback.print_exc())
            return json.dumps({"error": error_message}), 500


async def async_get_text(url, headers=None):
    """
        Gets text response from url asyncronously
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                logger.error(f'Failed to get response from {url}, returned status : {response.status}')
                return ''
            return await response.text()


async def async_get_response(url, headers=None, timeout=5*60):
    """
    Returns the whole reponse object
    """
    client_timeout = aiohttp.ClientTimeout(connect=timeout)
    async with aiohttp.ClientSession(timeout=client_timeout) as session:
        async with session.get(url, headers=headers) as response:
            try:
                json = await response.json()
            except JSONDecodeError:
                json = {}
            try:
                text = await response.text()
            except:
                text = ''
            try:
                raw = await response.read()
            except:
                raw = ''
            return {
                'headers': response.headers,
                'json': json,
                'text': text,
                'raw': raw,
                'status': response.status
            }
