import helper
import logging
import graphing
from telebot import types
import matplotlib.pyplot as plt
import time
import numpy as np
import os

def viewOverallBudget(chat_id, bot):
    if not helper.isCategoryBudgetAvailable(chat_id):
        bot.send_message(chat_id, "No category budget available", reply_markup=types.ReplyKeyboardRemove())
        return
    category_budget = {}
    for cat in helper.spend_categories:
        if helper.isCategoryBudgetByCategoryAvailable(chat_id, cat):
            category_budget[cat] = helper.getCategoryBudgetByCategory(chat_id, cat)
    
    graphing.overall_split(category_budget)
    bot.send_photo(chat_id, photo=open("overall_split.png", 'rb'), reply_markup=types.ReplyKeyboardRemove())
    os.remove("overall_split.png")

def viewSpendWise(chat_id, bot):
    category_spend = {}
    for cat in helper.spend_categories:
        spend = helper.calculate_total_spendings_for_cateogory_chat_id(chat_id,cat)
        if spend != 0:
            category_spend[cat] = spend

    if category_spend == {}:
        bot.send_message(chat_id, "No category spend available", reply_markup=types.ReplyKeyboardRemove())
        return
    graphing.spend_wise_split(category_spend)
    bot.send_photo(chat_id, photo=open("spend_wise.png", 'rb'), reply_markup=types.ReplyKeyboardRemove())
    os.remove("spend_wise.png")

def viewRemaining(chat_id, bot):
    if not helper.isCategoryBudgetAvailable(chat_id):
        bot.send_message(chat_id, "No category budget available", reply_markup=types.ReplyKeyboardRemove())
        return
    category_spend_percent = {}
    for cat in helper.spend_categories:
        if helper.isCategoryBudgetByCategoryAvailable(chat_id, cat):
            percent = helper.calculateRemainingCateogryBudgetPercent(chat_id, cat)
            category_spend_percent[cat] = percent
    graphing.remaining(category_spend_percent)
    bot.send_photo(chat_id, photo=open("remaining.png", 'rb'), reply_markup=types.ReplyKeyboardRemove())
    os.remove("remaining.png")

def viewHistory(chat_id, bot):
    if not helper.getUserHistory(chat_id):
        bot.send_message(chat_id, "No history available", reply_markup=types.ReplyKeyboardRemove())
        return
    
    cat_spend_dict = helper.getUserHistoryDateExpense(chat_id)

    graphing.time_series(cat_spend_dict)
    bot.send_photo(chat_id, photo=open("time_series.png", 'rb'), reply_markup=types.ReplyKeyboardRemove())
    os.remove("time_series.png")