import argparse
import sys
import gc
from transformers import MarianMTModel, MarianTokenizer
import torch


def main():
    parser = argparse.ArgumentParser(prog='opus-mt-translate')
    parser.add_argument('--device', default='cuda', type=str, help='Device to use. (cpu, cuda, cuda:1, etc)')
    parser.add_argument('--batch_size', default=16, type=int, help='Batch size.')
    parser.add_argument('--beam_size', default=5, type=int, help='Beam size.')
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s','--src-lang', help='Source language.')
    group.add_argument('static_src_lang', nargs='?', default='ru', help='Source language.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t','--target-lang', help='Target language.')
    group.add_argument('static_target_lang', nargs='?', default='en', help='Target language.')

    args = parser.parse_args()

    src_lang = args.src_lang or args.static_src_lang
    target_lang = args.target_lang or args.static_target_lang
    
    with torch.no_grad():
        model_name = 'Helsinki-NLP/opus-mt-{}-{}'.format(src_lang, target_lang)
        tokenizer = MarianTokenizer.from_pretrained(model_name)

        model = MarianMTModel.from_pretrained(model_name)
        model.eval()
        model.to(args.device)

        if args.device != 'cpu':
            # Fallback model
            model_cpu = MarianMTModel.from_pretrained(model_name)
            model_cpu.eval()

        def _translate_sents(sents):
            gc.collect()
            torch.cuda.empty_cache()
            
            try:
                inputs = tokenizer(sents, truncation=True, padding=True, max_length=None, return_tensors="pt")

                for key in inputs:
                    inputs[key] = inputs[key].to(args.device)

                translated = model.generate(**inputs, num_beams=args.beam_size)
                return [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
            except:

                inputs = tokenizer(sents, truncation=True, padding=True, max_length=None, return_tensors="pt")

                for key in inputs:
                    inputs[key] = inputs[key]

                translated = model_cpu.generate(**inputs, num_beams=args.beam_size)
                return [tokenizer.decode(t, skip_special_tokens=True) for t in translated]

        _sents = []   
        for line in sys.stdin:
            _sents.append(line)
            if len(_sents) == args.batch_size:
                print('\n'.join(_translate_sents(_sents)))
                _sents = []

        if len(_sents) > 0:
            print('\n'.join(_translate_sents(_sents)))
