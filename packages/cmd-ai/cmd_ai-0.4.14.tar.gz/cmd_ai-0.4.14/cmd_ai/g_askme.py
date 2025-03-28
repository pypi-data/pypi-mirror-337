#!/usr/bin/env python3

import datetime as dt
import time
import os
import tiktoken
from console import fg,bg,fx
from fire import Fire
import pandas as pd
import sys
import json # for function call
from fire import Fire

#import openai
from openai import OpenAI
from console import fg, bg, fx

from cmd_ai import config, texts, api_key
from cmd_ai import  function_chmi, function_goog, function_webc, function_calendar,function_gmail


import anthropic
from cmd_ai.api_key import get_api_key_anthropic


########################################################
config.available_functions = {
    "getCzechWeather": function_chmi.get_chmi, #
    "searchGoogle": function_goog.get_google_urls, #
    "getWebContent": function_webc.fetch_url_content, #
    "setMeetingRecord": function_calendar.setMeetingRecord, # i
    "sendGmail": function_gmail.sendGmail, #
    "getTodaysDateTime": function_calendar.getTodaysDateTime, #
}


# ===========================================================================
#   generated :  calculate price   GENERATED FROM ORG FILE
# ---------------------------------------------------------------------------
def get_price(model_name, input_tokens=0, output_tokens=0):
    """
    generated from the org  table by AI
    """
    data = {'Model': ['gpt-4o', 'gpt-4o-2024-08-06', 'gpt-4o-2024-11-20', 'gpt-4o-2024-08-06', 'gpt-4o-2024-05-13', 'gpt-4o-audio-preview', 'gpt-4o-audio-preview-2024-12-17', 'gpt-4o-audio-preview-2024-12-17', 'gpt-4o-audio-preview-2024-10-01', 'gpt-4o-realtime-preview', 'gpt-4o-realtime-preview-2024-12-17', 'gpt-4o-realtime-preview-2024-12-17', 'gpt-4o-realtime-preview-2024-10-01', 'gpt-4o-mini', 'gpt-4o-mini-2024-07-18', 'gpt-4o-mini-2024-07-18', 'gpt-4o-mini-audio-preview', 'gpt-4o-mini-audio-preview-2024-12-17', 'gpt-4o-mini-audio-preview-2024-12-17', 'gpt-4o-mini-realtime-preview', 'gpt-4o-mini-realtime-preview-2024-12-17', 'gpt-4o-mini-realtime-preview-2024-12-17', 'o1', 'o1-2024-12-17', 'o1-2024-12-17', 'o1-preview-2024-09-12', 'o1-mini', 'o1-mini-2024-09-12', 'o1-mini-2024-09-12', 'o3-mini-2025-01-31', 'gpt-4.5-preview', 'gpt-4.5-preview-2025-02-27'], 'Input Price': [2.5, 2.5, 2.5, 2.5, 5.0, 2.5, 2.5, 2.5, 2.5, 5.0, 5.0, 5.0, 5.0, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.6, 0.6, 0.6, 15.0, 15.0, 15.0, 15.0, 3.0, 3.0, 3.0, 1.1, 75.0, 75.0], 'Output Price': [10.0, 10.0, 10.0, 10.0, 15.0, 10.0, 10.0, 10.0, 10.0, 20.0, 20.0, 20.0, 20.0, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 2.4, 2.4, 2.4, 60.0, 60.0, 60.0, 60.0, 12.0, 12.0, 12.0, 4.4, 150.0, 150.0]
             }
    df = pd.DataFrame(data)
    model_row = df[df['Model'] == model_name]

    if model_row.empty:
        return 0 #"Model not found."

    input_price = model_row['Input Price'].values[0]
    output_price = model_row['Output Price'].values[0]

    total_price = (input_tokens / 1_000_000) * input_price + (output_tokens / 1_000_000) * output_price

    return total_price



# ===============================================================================================
def log_price(model, tokens_in = 1, tokens_out = 1):
    price = round(100000*get_price( model, tokens_in, tokens_out ))/100000
    with open( os.path.expanduser( config.CONFIG['pricelog']), "a" )  as f:
        now = dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        f.write(f"{now} {tokens_in} {tokens_out} {price}")
        f.write("\n")


# ============================================================
#
# ------------------------------------------------------------
#
def execute_function_call(function_name,arguments):
    """
    colorful call ...
    """
    print("i... executing  ", bg.red, fg.white, function_name, bg.default, fg.default, arguments)
    function = config.available_functions.get(function_name,None)
    if function:
        #print("i+++ executing function:   ", function_name)
        arguments = json.loads(arguments)
        #if config.DEBUG: print("i--- running ", arguments )
        results = function(**arguments)
        #print("r... results size=", sys.getsizeof(results))
    else:
        print("X---  executing function:   ", function_name)
        results = f"Error: function {function_name} does not exist"
    return results



# ============================================================
#    for debugging
# ------------------------------------------------------------
#
def xprint(x, style, level=0):
    SPC = " " * level * 5
    #print(f"{SPC}============================================================")
    print(style, end="")
    print( f"{SPC}... {x}", fg.default, bg.default, fx.default)
    #print()
    #print("------------------------------------------------------------")


# ============================================================
#
# ------------------------------------------------------------
#
# model="claude-3-7-sonnet-20250219"
# model="claude-3-5-sonnet-20241022"
def g_ask_claude(prompt , temp=0,
                 model="claude-3-7-sonnet-20250219",
                 role=None):
    # ** init
    clientanthropic = anthropic.Anthropic(api_key=get_api_key_anthropic())

    system_prompt = texts.role_assistant
    if role is None:
        system_prompt = texts.role_assistant
    # my message system (may be difference in naming)
    nmsg = []
    for i in config.messages:
        nmsg.append( i )

    nmsg.append({"role": "user", "content": [{"type": "text", "text": prompt}] } )
    limit_tokens = config.CONFIG['limit_tokens']

    #********************************************** GO
    message = clientanthropic.messages.create(
        model=model,
        max_tokens=limit_tokens,
        temperature=temp,
        system=system_prompt,
        messages=newmsg
    )
    # **********
    response = message.content
    res = response[0].text #decode_response_anthropic(message.content)

    return res




# ============================================================
# ============================================================
# ============================================================
# ============================================================
# ============================================================
#
# ------------------------------------------------------------
#
def g_ask_chat(prompt,  model, temp=0):
#def main():
    """
    ************************************ MAIN FUNCTION FOR CHAAT **********
    RETURNS :  response, reason_to_stop,  model_used
    """
    # assure the starting conditions *********** added for g_ask.
    if len(config.messages) == 0:
        config.messages.append({"role": "assistant", "content": texts.role_assistant})
    # ADD PROMPT
    config.messages.append({"role": "user", "content": prompt})
    limit_tokens = config.CONFIG['limit_tokens']
    if limit_tokens < 30000: # ;max_tokens
        max_tokens = limit_tokens
    else:
        max_tokens = 300

    # FORCE MODEL TO SYNC
    config.MODEL_TO_USE = model

    if not config.silent:
        print("...",bg.green," >>OK", bg.default, f" model={model}")

    if config.MODEL_TO_USE.find("claude") >= 0:
        res = g_ask_claude( prompt, temp, config.MODEL_TO_USE, estimate_tokens)
        if not config.silent:
            print("...",bg.green," >>OK", bg.default, f" model={model}")
        return res, "stop", config.MODEL_TO_USE

    # ----------------------------- DEBUGS ------------------
    PRINT_FULL_MESSAGES = False
    PRINT_RESPONSES = False # aqua ChatCompletion()   when tool is required
    # always print reason
    PRINT_TOOL_RESULTS = False # PINK  n: [ tool list ]
    # --------------------------- ADD TOOLS ------------------
    # ----this comes with .g ****************************
    #if len(config.TOOLLIST)==0:
    #    config.TOOLLIST = [ texts.tool_getCzechWeather, texts.tool_setMeetingRecord, texts.tool_sendGmail, texts.tool_getTodaysDateTime, texts.tool_searchGoogle, texts.tool_getWebContent]

    # ====== I CLEAR STUFF ******************** PUT THIS BACK ON  IF EXPLORING
    #model = "gpt-4o-2024-11-20"
    #max_tokens = 2000
    #config.messages.append({"role": "assistant", "content": texts.role_assistant})
    #config.messages.append( {"role":"user", "content":"Is bitwarden secure? Check the web for information from last 6 months."} )
    #temp = 0.0
    #config.client = OpenAI(api_key=api_key.get_api_key())

    # my statistics
    ntoolcalls = 0
    toolcalls_datasize = 0
    total_tokens_in = 0
    total_tokens_out = 0



    # IMPORTANT THINGS variables used over the function
    resp_content = "nil"
    resp_reason = "x"
    tokens_out = 0
    tokens_in = 0
    tokens = 0

    ### ENTRY POINT FOR LOOP
    KEEP_LOOPING = True
    while KEEP_LOOPING:
        #xprint(config.messages[-1], fg.cyan)
        if PRINT_FULL_MESSAGES:
            xprint(config.messages, fg.white)

        responded = False
        kill_me_on_0 = 3
        try:
            # MODEL
            response = config.client.chat.completions.create(
                model=model,
                messages=config.messages,
                temperature=temp,
                max_tokens=max_tokens,
                tool_choice="auto",
                tools= config.TOOLLIST
            )
            responded = True

        except openai.RateLimitError as e:
            if hasattr(e,"code"): print("  rateLimit...", e.code)
            if hasattr(e,"type"): print("  rateLimit...", e.type)
            print(f"Rate limit exceeded. Retrying in {retry_time} seconds...")
            time.sleep(5)
            kill_me_on_0 -= 1

        except openai.APIError as e:
            if hasattr(e,"code"): print(" ... API - error code:", e.code)
            if hasattr(e,"type"): print(" ... API - error type:", e.type)
            print(f" ... API error occurred. Retrying in {retry_time} seconds...")
            print(" ... ... might be for difficulties when calling a tool? Unallowd options?")
            time.sleep( 5)
            kill_me_on_0 -= 1

        except openai.ServiceUnavailableError as e:
            if hasattr(e,"code"): print(" ...ServiceUnavailable...", e.code)
            if hasattr(e,"type"): print(" ...ServiceUnavailable...", e.type)
            print(f"Service is unavailable. Retrying in {retry_time} seconds...")
            time.sleep(5)
            kill_me_on_0 -= 1

        except openai.Timeout as e:
            if hasattr(e,"code"): print("... Timeout...", e.code)
            if hasattr(e,"type"): print("... Timeout...", e.type)
            print(f"Request timed out: {e}. Retrying in {retry_time} seconds...")
            time.sleep(5)
            kill_me_on_0 -= 1

        except OSError as e:
            if isinstance(e, tuple) and len(e) == 2 and isinstance(e[1], OSError):
                if hasattr(e,"code"): print("... OSError...", e.code)
                if hasattr(e,"type"): print("... OSError...", e.type)
                print(f"Connection error occurred: {e}. Retrying in {retry_time} seconds...")
                time.sleep(5)
                kill_me_on_0 -= 1
            else:
                print(f"Connection error occurred: {e}. Retrying in {retry_time} seconds...")
                time.sleep(5)
                kill_me_on_0 -= 1
                raise e

        if kill_me_on_0 <= 0:
            sys.exit(1)

        if not responded:
            continue

        # ALL EXCEPTIONS DONE AND SOLVED **********************
        if PRINT_FULL_MESSAGES:
            xprint(response, fg.white + fx.italic)

        resp_content = response.choices[0].message.content
        resp_reason = response.choices[0].finish_reason
        tokens_out = response.usage.completion_tokens
        tokens_in = response.usage.prompt_tokens
        total_tokens_in += tokens_in
        total_tokens_out += tokens_out
        tokens = response.usage.total_tokens

        if resp_content is not None: # Dont report None conntent....it is tools....
            if PRINT_RESPONSES: xprint(resp_content, fg.yellow)
        if resp_reason != "stop": # Dont report standard stop reason
            xprint(resp_reason, fg.red) # always print reason

        # ****************** TOOLCALLS*******************
        if resp_reason == "tool_calls":
            resp_message = response.choices[0].message
            tool_calls = response.choices[0].message.tool_calls
            if PRINT_RESPONSES:
                xprint(resp_message, fg.aquamarine)
            config.messages.append( resp_message ) # ASPPENDING THIS TO CHAT!!!
            if PRINT_TOOL_RESULTS:
                xprint(f" {len(tool_calls)}: {tool_calls}", fg.pink)
            if len(tool_calls) > 0:
                for tool_call in tool_calls:
                    fun_name = tool_call.function.name
                    fun_to_call = config.available_functions[fun_name]
                    fun_args = tool_call.function.arguments # NO json.loads
                    fun_response = execute_function_call( fun_name, fun_args  )
                    ntoolcalls += 1
                    toolcalls_datasize += sys.getsizeof(fun_response)
                    #
                    #if len(fun_response) > 1000:
                    #    run_response = fun_response[:1000]
                    #
                    #xprint(fun_response, fg.lime, level=1) # this is just my function output....
                    GEN_MESSAGE = {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": fun_name,
                        "content": fun_response,
                    }
                    config.messages.append( GEN_MESSAGE ) # ASPPENDING THIS TO CHAT!!!

                # NOW ALL TOOL CALLS ARE FINISHED.....
                # xprint(config.messages, fg.orchid)
                # response = config.client.chat.completions.create(
                #     model=model,
                #     messages=config.messages,
                #     temperature=temp,
                #     max_tokens=max_tokens,
                #     tool_choice="auto",
                #     tools= config.TOOLLIST
                # )
                # xprint(response, fg.white)
                # resp_content = response.choices[0].message.content
                # resp_reason = response.choices[0].finish_reason
                # xprint(resp_content, fg.orange)
                # xprint(resp_reason, fg.red)
                # GOES TO WHILE START
            else:
                print("X... tools requested but ???... no tool_calls prepared ???")
                KEEP_LOOPING = False
                sys.exit(1)
        elif resp_reason == "stop":
            KEEP_LOOPING = False # go home after all done
        else:
            print("X... other reason ... resp_reason == {resp_reason} ")
            KEEP_LOOPING = False # go home after all done



    # ----------------- While loop ends here ------------------------
    price = get_price( model, total_tokens_in, total_tokens_out)
    print(f"i... {fg.dimgray}TOOLS   {ntoolcalls} x called ... TOTAL data size {toolcalls_datasize}    total tokens={total_tokens_in+total_tokens_out} for {price:.4f} $ {fg.default}")
    log_price( model, total_tokens_in, total_tokens_out )
    #xprint(resp_content, fg.lime) # REAL LAST RESPONSE
    if not config.silent:
        print("...",bg.green," >>OK", bg.default, f" model={model}")
    return resp_content, resp_reason, config.MODEL_TO_USE



def main():
    """
    for Fire
    """
    config.client = OpenAI(api_key=api_key.get_api_key())
    g_ask_chat("Hi", model = "gpt-4o-2024-11-20", temp=0)


# ============================================================
#
# ------------------------------------------------------------
#
if  __name__ == "__main__":
    Fire(main)
