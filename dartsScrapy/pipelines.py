# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class DartsscrapyPipeline(object):
#     def process_item(self, item, spider):
#         return item


class ProcessPipeline(object):
    def process_item(self, item, spider):
        if item.get('playersNames'):
        	# print(item.get('playersNames'))

            names = item.get('playersNames')
            names = names.split(' - ')
            # Player1 Name cleaning
            if (len(names[0].strip().split(' ')) > 1):
                item['player1'] = names[0].strip().split(' ')[:-1]
                item['player1Initial'] = names[0].strip().split(' ')[-1][0].lower().strip()
                # Edge cases where the player name may have 2 initials
                if "." in (names[0].strip().split(' ')[-2]):
                    item['player1'] = names[0].strip().split(' ')[:-2]
                    item['player1Initial'] = names[0].strip().split(' ')[-2].lower().strip()
                    item['player1Initial'] = item['player1Initial'].replace('.', '')
                item['player1'] = ' '.join(item['player1'])
            else:
                item['player1'] = names[0].strip().split(' ')[0]
                item['player1Initial'] = names[0].strip().split(' ')[-1][0].lower().strip()

            # Player2 Name cleaning                
            if (len(names[0].strip().split(' ')) > 1):
                item['player2'] = names[1].strip().split(' ')[:-1]
                item['player2Initial'] = names[1].strip().split(' ')[-1][0].lower().strip()
                # Edge cases where the player name may have 2 initials
                if "." in (names[1].strip().split(' ')[-2]):
                    item['player2'] = names[1].strip().split(' ')[:-2]
                    item['player2Initial'] = names[1].strip().split(' ')[-2].lower().strip()
                    item['player2Initial'] = item['player2Initial'].replace('.', '')
                item['player2'] = ' '.join(item['player2'])
            else:
                item['player2'] = names[1].strip().split(' ')[0]
                item['player2Initial'] = names[1].strip().split(' ')[-1][0].lower().strip()

        if item.get('score'):

	        outcome = item.get('score').strip().split(':')
	        player1score = int(float(outcome[0]))
	        player2score = int(float(outcome[1]))

	        if(player1score == player2score):
	            item['outcome'] = '2'
	        elif(player1score > player2score):
	            item['outcome'] = '1'
	        elif(player1score < player2score):
	            item['outcome'] = '0'
	        else:
	            item['outcome'] = None
        return item